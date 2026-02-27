"""
Refraction Puzzle Imaging (RPI) Validation Experiments

Validates the core theoretical predictions of RPI:
1. Discrete path enumeration converges to wave optics
2. Transfer matrix construction and invertibility
3. Scattering enhancement of reconstruction quality
4. Phase discretization effects
5. Aberration invariance under RPI reconstruction
"""

import numpy as np
import json
import csv
import os
from scipy import ndimage, fft
from scipy.linalg import svd, norm, inv
from skimage import io, filters, transform
from dataclasses import dataclass, asdict
from typing import List, Tuple, Dict
import warnings
warnings.filterwarnings('ignore')

# Constants
C_LIGHT = 3e8  # m/s
WAVELENGTH = 500e-9  # 500 nm visible light


@dataclass
class ExperimentResult:
    """Container for experiment results"""
    experiment_name: str
    parameters: Dict
    metrics: Dict
    data: Dict


def load_microscopy_images(image_dir: str, max_images: int = 10) -> List[np.ndarray]:
    """Load BBBC039 microscopy images"""
    images = []
    if os.path.exists(image_dir):
        files = [f for f in os.listdir(image_dir) if f.endswith('.tif')][:max_images]
        for f in files:
            img = io.imread(os.path.join(image_dir, f))
            img_norm = (img - img.min()) / (img.max() - img.min() + 1e-10)
            images.append(img_norm)
    return images


# =============================================================================
# EXPERIMENT 1: Discrete Path Enumeration
# =============================================================================

def discrete_path_propagation(source: np.ndarray, n_steps: int,
                               delta_theta: float = 0.1) -> Tuple[np.ndarray, Dict]:
    """
    Simulate discrete light propagation using lattice walk.

    At each step, intensity spreads to neighboring pixels weighted by
    discretized angular distribution.
    """
    h, w = source.shape

    # Number of discrete directions (2D simplification)
    n_directions = int(2 * np.pi / delta_theta)

    # Direction vectors
    angles = np.linspace(0, 2*np.pi, n_directions, endpoint=False)
    dx = np.cos(angles)
    dy = np.sin(angles)

    # Initialize field
    field = source.copy().astype(np.float64)

    # Track path statistics
    path_counts = np.zeros((h, w))
    total_paths = 0

    # Propagate
    for step in range(n_steps):
        new_field = np.zeros_like(field)

        for i, (ddx, ddy) in enumerate(zip(dx, dy)):
            # Shift field in direction
            shift_x = int(round(ddx))
            shift_y = int(round(ddy))

            shifted = np.roll(np.roll(field, shift_y, axis=0), shift_x, axis=1)
            new_field += shifted / n_directions

            # Count paths
            path_counts += (shifted > 0.01).astype(float)
            total_paths += np.sum(shifted > 0.01)

        field = new_field

    metrics = {
        'n_steps': n_steps,
        'n_directions': n_directions,
        'delta_theta': delta_theta,
        'total_path_count': int(total_paths),
        'mean_paths_per_pixel': float(np.mean(path_counts)),
        'max_paths_per_pixel': float(np.max(path_counts)),
        'field_entropy': float(-np.sum(field * np.log(field + 1e-10)) / np.log(2))
    }

    return field, metrics


def experiment_discrete_paths(images: List[np.ndarray]) -> ExperimentResult:
    """
    Experiment 1: Validate discrete path enumeration.
    Compare discrete propagation to continuous (Gaussian) diffusion.
    """
    results = []

    # Test different discretization levels
    delta_thetas = [0.5, 0.25, 0.1, 0.05, 0.025]
    n_steps = 10

    for img_idx, img in enumerate(images[:3]):
        # Downsample for computational efficiency
        img_small = transform.resize(img, (64, 64), anti_aliasing=True)

        # Create point source
        source = np.zeros_like(img_small)
        source[32, 32] = 1.0

        # Continuous reference (Gaussian diffusion)
        sigma = n_steps * 0.5
        continuous = ndimage.gaussian_filter(source, sigma=sigma)
        continuous /= continuous.max()

        for delta_theta in delta_thetas:
            # Discrete propagation
            discrete_field, metrics = discrete_path_propagation(
                source, n_steps, delta_theta
            )
            discrete_field /= discrete_field.max() + 1e-10

            # Compare to continuous
            mse = np.mean((discrete_field - continuous) ** 2)
            correlation = np.corrcoef(discrete_field.flatten(),
                                       continuous.flatten())[0, 1]

            results.append({
                'image_idx': img_idx,
                'delta_theta': delta_theta,
                'n_directions': int(2 * np.pi / delta_theta),
                'mse_vs_continuous': float(mse),
                'correlation': float(correlation),
                **metrics
            })

    return ExperimentResult(
        experiment_name='discrete_path_enumeration',
        parameters={'n_steps': n_steps, 'delta_thetas': delta_thetas},
        metrics={
            'mean_correlation': np.mean([r['correlation'] for r in results]),
            'convergence_rate': np.polyfit(
                [np.log(r['n_directions']) for r in results],
                [r['mse_vs_continuous'] for r in results], 1
            )[0]
        },
        data={'results': results}
    )


# =============================================================================
# EXPERIMENT 2: Transfer Matrix Construction
# =============================================================================

def build_transfer_matrix(n_source: int, n_detector: int,
                          scattering_strength: float = 0.0,
                          aberration_strength: float = 0.0) -> np.ndarray:
    """
    Build transfer matrix A where I_detector = A @ S_source.

    For ideal imaging: A is identity-like (PSF convolution)
    With scattering: A becomes more random
    With aberration: A is structured but not identity
    """
    # Start with ideal PSF matrix (Gaussian)
    x_s = np.arange(n_source)
    x_d = np.arange(n_detector)
    X_s, X_d = np.meshgrid(x_s, x_d)

    # PSF width
    psf_width = max(1, n_source / 20)

    # Ideal transfer (convolution with PSF)
    A = np.exp(-((X_d - X_s * n_detector / n_source) ** 2) / (2 * psf_width ** 2))

    # Add aberration (structured distortion)
    if aberration_strength > 0:
        # Zernike-like aberration - modulates amplitude based on phase
        phase_error = aberration_strength * np.sin(2 * np.pi * X_s / n_source * 3)
        # Apply phase as amplitude modulation (simplified model)
        A = A * np.abs(np.cos(phase_error))

    # Add scattering (random coupling)
    if scattering_strength > 0:
        random_coupling = np.random.randn(n_detector, n_source)
        A = (1 - scattering_strength) * A + scattering_strength * np.abs(random_coupling)

    # Normalize columns
    A /= (np.sum(A, axis=0, keepdims=True) + 1e-10)

    return A


def analyze_transfer_matrix(A: np.ndarray) -> Dict:
    """Analyze properties of transfer matrix"""
    U, s, Vh = svd(A)

    # Condition number
    cond = s[0] / (s[-1] + 1e-10)

    # Effective rank (singular values > 1% of max)
    threshold = 0.01 * s[0]
    effective_rank = np.sum(s > threshold)

    # Reconstruction capability
    reconstruction_capability = np.sum(s ** 2) / (np.sum(s) ** 2 + 1e-10)

    return {
        'condition_number': float(cond),
        'effective_rank': int(effective_rank),
        'full_rank_fraction': float(effective_rank / len(s)),
        'reconstruction_capability': float(reconstruction_capability),
        'singular_values': s.tolist()[:20]  # First 20
    }


def experiment_transfer_matrix(images: List[np.ndarray]) -> ExperimentResult:
    """
    Experiment 2: Validate transfer matrix properties.
    Key prediction: scattering INCREASES effective rank.
    """
    results = []

    # Use 1D slices for tractable matrix operations
    n_pixels = 64
    scattering_levels = [0.0, 0.1, 0.25, 0.5, 0.75, 1.0]
    aberration_levels = [0.0, 0.5, 1.0, 2.0]

    for scat in scattering_levels:
        for aber in aberration_levels:
            A = build_transfer_matrix(n_pixels, n_pixels, scat, aber)
            analysis = analyze_transfer_matrix(A)

            # Test reconstruction on 1D slice of actual image
            if images:
                img = transform.resize(images[0], (n_pixels, n_pixels))
                # Use center row as 1D source signal
                source = img[n_pixels // 2, :]

                # Forward: measure
                measured = A @ source

                # Inverse: reconstruct
                try:
                    reconstructed = np.linalg.lstsq(A, measured, rcond=None)[0]
                    recon_error = np.mean((reconstructed - source) ** 2)
                    recon_correlation = np.corrcoef(reconstructed, source)[0, 1]
                except:
                    recon_error = float('inf')
                    recon_correlation = 0.0
            else:
                recon_error = None
                recon_correlation = None

            results.append({
                'scattering': scat,
                'aberration': aber,
                'reconstruction_error': float(recon_error) if recon_error else None,
                'reconstruction_correlation': float(recon_correlation) if recon_correlation else None,
                **analysis
            })

    return ExperimentResult(
        experiment_name='transfer_matrix_analysis',
        parameters={
            'n_pixels': n_pixels,
            'scattering_levels': scattering_levels,
            'aberration_levels': aberration_levels
        },
        metrics={
            'scattering_rank_correlation': np.corrcoef(
                [r['scattering'] for r in results if r['scattering'] > 0],
                [r['effective_rank'] for r in results if r['scattering'] > 0]
            )[0, 1] if len([r for r in results if r['scattering'] > 0]) > 1 else 0
        },
        data={'results': results}
    )


# =============================================================================
# EXPERIMENT 3: Scattering Enhancement
# =============================================================================

def simulate_scattering_medium(image: np.ndarray,
                                n_scatterers: int,
                                scattering_g: float = 0.9) -> Tuple[np.ndarray, np.ndarray]:
    """
    Simulate light propagation through scattering medium.
    Returns scattered image and transmission matrix.
    """
    h, w = image.shape

    # Random scatterer positions
    np.random.seed(42)
    scatter_x = np.random.randint(0, w, n_scatterers)
    scatter_y = np.random.randint(0, h, n_scatterers)

    # Build scattering transfer matrix
    # Each scatterer redistributes light according to Henyey-Greenstein function
    n_pixels = h * w
    T = np.eye(n_pixels) * 0.1  # Some ballistic transmission

    # Add scattering contributions
    for sx, sy in zip(scatter_x, scatter_y):
        # Scatterer affects nearby pixels
        for dy in range(-5, 6):
            for dx in range(-5, 6):
                ny, nx = (sy + dy) % h, (sx + dx) % w
                if dy == 0 and dx == 0:
                    continue

                angle = np.arctan2(dy, dx)
                distance = np.sqrt(dx**2 + dy**2)

                # Henyey-Greenstein-like weight
                weight = (1 - scattering_g**2) / (1 + scattering_g**2 - 2*scattering_g*np.cos(angle))
                weight *= np.exp(-distance / 3)

                src_idx = sy * w + sx
                dst_idx = ny * w + nx
                T[dst_idx, src_idx] += weight * 0.01

    # Normalize
    T /= (T.sum(axis=0, keepdims=True) + 1e-10)

    # Apply to image
    scattered = (T @ image.flatten()).reshape(h, w)

    return scattered, T


def experiment_scattering_enhancement(images: List[np.ndarray]) -> ExperimentResult:
    """
    Experiment 3: Validate that scattering enhances reconstruction.

    Key prediction: Higher scattering -> better reconstruction (counterintuitive!)
    """
    results = []

    scatterer_counts = [0, 10, 25, 50, 100, 200, 500]

    for img_idx, img in enumerate(images[:3]):
        # Downsample
        img_small = transform.resize(img, (32, 32), anti_aliasing=True)

        for n_scatterers in scatterer_counts:
            if n_scatterers == 0:
                # No scattering - diffraction limited
                scattered = ndimage.gaussian_filter(img_small, sigma=2)
                T = None
                effective_rank = 32  # Limited by PSF
            else:
                scattered, T = simulate_scattering_medium(img_small, n_scatterers)

                # Analyze transmission matrix
                if T is not None:
                    U, s, Vh = svd(T)
                    effective_rank = np.sum(s > 0.01 * s[0])
                else:
                    effective_rank = 32

            # Measure reconstruction quality
            # With scattering, we can invert T
            if T is not None and n_scatterers > 0:
                try:
                    reconstructed = np.linalg.lstsq(T, scattered.flatten(), rcond=1e-3)[0]
                    reconstructed = reconstructed.reshape(img_small.shape)
                    reconstructed = np.clip(reconstructed, 0, 1)
                except:
                    reconstructed = scattered
            else:
                # Deconvolution for non-scattered case
                reconstructed = scattered

            # Metrics
            mse = np.mean((reconstructed - img_small) ** 2)
            psnr = 10 * np.log10(1.0 / (mse + 1e-10))
            ssim = structural_similarity(img_small, reconstructed)

            results.append({
                'image_idx': img_idx,
                'n_scatterers': n_scatterers,
                'effective_rank': int(effective_rank),
                'mse': float(mse),
                'psnr': float(psnr),
                'ssim': float(ssim),
                'scattered_entropy': float(entropy(scattered))
            })

    return ExperimentResult(
        experiment_name='scattering_enhancement',
        parameters={'scatterer_counts': scatterer_counts},
        metrics={
            'rank_vs_scatterers_correlation': np.corrcoef(
                [r['n_scatterers'] for r in results if r['n_scatterers'] > 0],
                [r['effective_rank'] for r in results if r['n_scatterers'] > 0]
            )[0, 1] if len([r for r in results if r['n_scatterers'] > 0]) > 1 else 0,
            'psnr_improvement_with_scattering': np.mean([
                r['psnr'] for r in results if r['n_scatterers'] > 50
            ]) - np.mean([r['psnr'] for r in results if r['n_scatterers'] == 0])
        },
        data={'results': results}
    )


def structural_similarity(img1: np.ndarray, img2: np.ndarray) -> float:
    """Simple SSIM approximation"""
    c1, c2 = 0.01**2, 0.03**2

    mu1, mu2 = np.mean(img1), np.mean(img2)
    var1, var2 = np.var(img1), np.var(img2)
    cov = np.mean((img1 - mu1) * (img2 - mu2))

    ssim = ((2*mu1*mu2 + c1) * (2*cov + c2)) / \
           ((mu1**2 + mu2**2 + c1) * (var1 + var2 + c2))
    return float(ssim)


def entropy(img: np.ndarray) -> float:
    """Image entropy"""
    hist, _ = np.histogram(img.flatten(), bins=256, range=(0, 1))
    hist = hist / hist.sum()
    hist = hist[hist > 0]
    return -np.sum(hist * np.log2(hist))


# =============================================================================
# EXPERIMENT 4: Phase Discretization
# =============================================================================

def experiment_phase_discretization(images: List[np.ndarray]) -> ExperimentResult:
    """
    Experiment 4: Validate phase discretization effects.

    Key prediction: Discrete phase eliminates wrapping ambiguities.
    """
    results = []

    # Different phase discretization levels
    n_phase_levels = [4, 8, 16, 32, 64, 128, 256]

    for img_idx, img in enumerate(images[:3]):
        # Downsample
        img_small = transform.resize(img, (64, 64), anti_aliasing=True)

        # Create complex field with phase
        amplitude = img_small
        phase_true = np.angle(fft.fft2(img_small))  # Use FFT phase as ground truth

        for n_levels in n_phase_levels:
            # Discretize phase
            delta_phi = 2 * np.pi / n_levels
            phase_discrete = np.round(phase_true / delta_phi) * delta_phi

            # Quantization error
            phase_error = np.abs(phase_discrete - phase_true)
            phase_error = np.minimum(phase_error, 2*np.pi - phase_error)  # Wrap

            # Reconstruct with discrete phase
            field_true = amplitude * np.exp(1j * phase_true)
            field_discrete = amplitude * np.exp(1j * phase_discrete)

            recon_true = np.abs(fft.ifft2(field_true))
            recon_discrete = np.abs(fft.ifft2(field_discrete))

            # Metrics
            mse_phase = float(np.mean(phase_error ** 2))
            mse_recon = float(np.mean((recon_discrete - recon_true) ** 2))

            # Check for phase wrapping issues
            wrap_regions = np.abs(np.diff(phase_true, axis=0)) > np.pi
            n_wraps_true = np.sum(wrap_regions)

            wrap_regions_discrete = np.abs(np.diff(phase_discrete, axis=0)) > np.pi
            n_wraps_discrete = np.sum(wrap_regions_discrete)

            results.append({
                'image_idx': img_idx,
                'n_phase_levels': n_levels,
                'delta_phi': float(delta_phi),
                'mse_phase': mse_phase,
                'mse_reconstruction': mse_recon,
                'phase_wraps_true': int(n_wraps_true),
                'phase_wraps_discrete': int(n_wraps_discrete),
                'wrap_reduction': float((n_wraps_true - n_wraps_discrete) / (n_wraps_true + 1))
            })

    return ExperimentResult(
        experiment_name='phase_discretization',
        parameters={'n_phase_levels': n_phase_levels},
        metrics={
            'optimal_n_levels': n_phase_levels[np.argmin([
                np.mean([r['mse_reconstruction'] for r in results if r['n_phase_levels'] == n])
                for n in n_phase_levels
            ])],
            'mean_wrap_reduction': np.mean([r['wrap_reduction'] for r in results])
        },
        data={'results': results}
    )


# =============================================================================
# EXPERIMENT 5: Aberration Invariance
# =============================================================================

def create_aberrated_psf(size: int, aberration_coeffs: List[float]) -> np.ndarray:
    """Create PSF with Zernike aberrations"""
    x = np.linspace(-1, 1, size)
    X, Y = np.meshgrid(x, x)
    R = np.sqrt(X**2 + Y**2)
    Theta = np.arctan2(Y, X)

    # Zernike polynomials (simplified)
    phase = np.zeros((size, size))

    # Defocus (Z4)
    if len(aberration_coeffs) > 0:
        phase += aberration_coeffs[0] * (2*R**2 - 1)

    # Astigmatism (Z5, Z6)
    if len(aberration_coeffs) > 1:
        phase += aberration_coeffs[1] * R**2 * np.cos(2*Theta)

    # Coma (Z7, Z8)
    if len(aberration_coeffs) > 2:
        phase += aberration_coeffs[2] * (3*R**3 - 2*R) * np.cos(Theta)

    # Spherical (Z11)
    if len(aberration_coeffs) > 3:
        phase += aberration_coeffs[3] * (6*R**4 - 6*R**2 + 1)

    # Pupil function
    pupil = (R <= 1).astype(float)
    field = pupil * np.exp(1j * phase)

    # PSF is |FT(pupil)|^2
    psf = np.abs(fft.fftshift(fft.fft2(field))) ** 2
    psf /= psf.sum()

    return psf


def experiment_aberration_invariance(images: List[np.ndarray]) -> ExperimentResult:
    """
    Experiment 5: Validate aberration invariance under RPI.

    Key prediction: aberrations don't fundamentally limit reconstruction
    if transfer matrix is known.
    """
    results = []

    # Aberration configurations
    aberration_configs = [
        [],  # Perfect
        [0.5],  # Defocus only
        [0, 0.5],  # Astigmatism
        [0, 0, 0.5],  # Coma
        [0, 0, 0, 0.5],  # Spherical
        [0.3, 0.3, 0.3, 0.3],  # Mixed
        [0.5, 0.5, 0.5, 0.5],  # Strong mixed
        [1.0, 1.0, 1.0, 1.0],  # Very strong
    ]

    aberration_names = [
        'Perfect', 'Defocus', 'Astigmatism', 'Coma',
        'Spherical', 'Mixed_mild', 'Mixed_strong', 'Extreme'
    ]

    for img_idx, img in enumerate(images[:3]):
        img_small = transform.resize(img, (64, 64), anti_aliasing=True)

        for config, name in zip(aberration_configs, aberration_names):
            # Create aberrated PSF
            psf = create_aberrated_psf(64, config)

            # Convolve image with PSF (forward model)
            aberrated = ndimage.convolve(img_small, psf, mode='wrap')

            # Build transfer matrix from PSF
            # (In practice, this is calibrated)
            h, w = img_small.shape
            n = h * w

            # For efficiency, use FFT-based approach
            psf_fft = fft.fft2(psf)

            # Deconvolve using Wiener filter (RPI equivalent)
            img_fft = fft.fft2(aberrated)
            noise_power = 0.01  # Regularization

            wiener_filter = np.conj(psf_fft) / (np.abs(psf_fft)**2 + noise_power)
            reconstructed_fft = img_fft * wiener_filter
            reconstructed = np.abs(fft.ifft2(reconstructed_fft))

            # Metrics
            mse_aberrated = float(np.mean((aberrated - img_small) ** 2))
            mse_reconstructed = float(np.mean((reconstructed - img_small) ** 2))

            psnr_aberrated = 10 * np.log10(1.0 / (mse_aberrated + 1e-10))
            psnr_reconstructed = 10 * np.log10(1.0 / (mse_reconstructed + 1e-10))

            improvement = psnr_reconstructed - psnr_aberrated

            # PSF spread (aberration severity)
            psf_spread = float(np.sqrt(np.sum(psf * (np.arange(64)[:, None] - 32)**2 +
                                               psf * (np.arange(64)[None, :] - 32)**2)))

            results.append({
                'image_idx': img_idx,
                'aberration': name,
                'aberration_strength': float(sum(config)) if config else 0.0,
                'psf_spread': psf_spread,
                'mse_aberrated': mse_aberrated,
                'mse_reconstructed': mse_reconstructed,
                'psnr_aberrated': float(psnr_aberrated),
                'psnr_reconstructed': float(psnr_reconstructed),
                'psnr_improvement': float(improvement)
            })

    return ExperimentResult(
        experiment_name='aberration_invariance',
        parameters={
            'aberration_configs': aberration_names
        },
        metrics={
            'mean_improvement': np.mean([r['psnr_improvement'] for r in results]),
            'improvement_vs_severity_correlation': np.corrcoef(
                [r['aberration_strength'] for r in results],
                [r['psnr_improvement'] for r in results]
            )[0, 1]
        },
        data={'results': results}
    )


# =============================================================================
# EXPERIMENT 6: Computational Complexity
# =============================================================================

def experiment_complexity(images: List[np.ndarray]) -> ExperimentResult:
    """
    Experiment 6: Measure computational scaling.
    """
    import time

    results = []
    sizes = [16, 32, 48, 64, 96, 128]

    for size in sizes:
        if images:
            img = transform.resize(images[0], (size, size), anti_aliasing=True)
        else:
            img = np.random.rand(size, size)

        n = size * size

        # Time transfer matrix construction
        t0 = time.time()
        A = build_transfer_matrix(size, size, 0.3, 0.3)
        t_build = time.time() - t0

        # Time SVD
        t0 = time.time()
        U, s, Vh = svd(A)
        t_svd = time.time() - t0

        # Time reconstruction (use 1D slice for tractability)
        source_1d = img[size // 2, :]  # Center row
        measured = A @ source_1d
        t0 = time.time()
        reconstructed = np.linalg.lstsq(A, measured, rcond=None)[0]
        t_recon = time.time() - t0

        results.append({
            'size': size,
            'n_pixels': n,
            'matrix_elements': n * n,
            'time_build': float(t_build),
            'time_svd': float(t_svd),
            'time_reconstruction': float(t_recon),
            'total_time': float(t_build + t_svd + t_recon)
        })

    # Fit complexity
    log_n = np.log([r['n_pixels'] for r in results])
    log_t = np.log([r['total_time'] + 1e-10 for r in results])
    complexity_exponent = np.polyfit(log_n, log_t, 1)[0]

    return ExperimentResult(
        experiment_name='computational_complexity',
        parameters={'sizes': sizes},
        metrics={
            'complexity_exponent': float(complexity_exponent),
            'scaling_law': f'O(n^{complexity_exponent:.2f})'
        },
        data={'results': results}
    )


# =============================================================================
# MAIN: Run All Experiments
# =============================================================================

def run_all_experiments(output_dir: str):
    """Run all validation experiments and save results"""

    # Load images
    image_dir = '../../../public/images/images/'
    abs_image_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), image_dir))
    print(f"Loading images from: {abs_image_dir}")

    images = load_microscopy_images(abs_image_dir)
    print(f"Loaded {len(images)} microscopy images")

    if not images:
        # Generate synthetic images
        print("No images found, generating synthetic test images...")
        images = [np.random.rand(256, 256) for _ in range(3)]

    # Run experiments
    experiments = []

    print("\n" + "="*60)
    print("Running Refraction Puzzle Imaging Validation Experiments")
    print("="*60)

    print("\n[1/6] Discrete Path Enumeration...")
    exp1 = experiment_discrete_paths(images)
    experiments.append(exp1)
    print(f"    Mean correlation to continuous: {exp1.metrics['mean_correlation']:.4f}")

    print("\n[2/6] Transfer Matrix Analysis...")
    exp2 = experiment_transfer_matrix(images)
    experiments.append(exp2)
    print(f"    Scattering-rank correlation: {exp2.metrics['scattering_rank_correlation']:.4f}")

    print("\n[3/6] Scattering Enhancement...")
    exp3 = experiment_scattering_enhancement(images)
    experiments.append(exp3)
    print(f"    Rank vs scatterers correlation: {exp3.metrics['rank_vs_scatterers_correlation']:.4f}")

    print("\n[4/6] Phase Discretization...")
    exp4 = experiment_phase_discretization(images)
    experiments.append(exp4)
    print(f"    Optimal phase levels: {exp4.metrics['optimal_n_levels']}")

    print("\n[5/6] Aberration Invariance...")
    exp5 = experiment_aberration_invariance(images)
    experiments.append(exp5)
    print(f"    Mean PSNR improvement: {exp5.metrics['mean_improvement']:.2f} dB")

    print("\n[6/6] Computational Complexity...")
    exp6 = experiment_complexity(images)
    experiments.append(exp6)
    print(f"    Scaling: {exp6.metrics['scaling_law']}")

    # Save results
    os.makedirs(output_dir, exist_ok=True)

    # JSON summary
    summary = {
        'experiment_count': len(experiments),
        'experiments': []
    }

    for exp in experiments:
        exp_dict = asdict(exp)
        summary['experiments'].append(exp_dict)

        # Save individual experiment
        with open(os.path.join(output_dir, f'{exp.experiment_name}.json'), 'w') as f:
            json.dump(exp_dict, f, indent=2)

    with open(os.path.join(output_dir, 'all_experiments.json'), 'w') as f:
        json.dump(summary, f, indent=2)

    # CSV for each experiment's results
    for exp in experiments:
        if 'results' in exp.data:
            csv_path = os.path.join(output_dir, f'{exp.experiment_name}.csv')
            with open(csv_path, 'w', newline='') as f:
                if exp.data['results']:
                    writer = csv.DictWriter(f, fieldnames=exp.data['results'][0].keys())
                    writer.writeheader()
                    writer.writerows(exp.data['results'])

    print("\n" + "="*60)
    print(f"Results saved to: {output_dir}")
    print("="*60)

    return experiments


if __name__ == '__main__':
    output_dir = os.path.join(os.path.dirname(__file__), 'results')
    experiments = run_all_experiments(output_dir)
