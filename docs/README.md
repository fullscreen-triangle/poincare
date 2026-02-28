# Poincaré Computing - GitHub Pages Site

This directory contains the GitHub Pages site for the Poincaré Computing framework.

## Setup

### Enable GitHub Pages

1. Go to your repository settings on GitHub
2. Navigate to "Pages" section
3. Under "Source", select "Deploy from a branch"
4. Choose "main" branch and "/docs" folder
5. Click "Save"

Your site will be available at: `https://fullscreen-triangle.github.io/poincare/`

### Local Preview

To preview the site locally:

```bash
# Using Python's built-in server
cd docs
python -m http.server 8000

# Or using Node.js http-server
npx http-server docs -p 8000

# Then open http://localhost:8000 in your browser
```

## Structure

```
docs/
├── index.html          # Main landing page
├── css/
│   └── style.css       # Styling
├── images/             # Visualizations
│   ├── panel_1_entropy_space.png
│   ├── panel_2_performance.png
│   ├── panel_3_complexity.png
│   ├── panel_4_distances.png
│   └── panel_5_comparative.png
└── README.md           # This file
```

## Features

- **Responsive Design**: Mobile-friendly layout
- **Modern UI**: Clean, professional appearance
- **Interactive Navigation**: Smooth scrolling
- **Performance Metrics**: Key results prominently displayed
- **Code Examples**: Syntax-highlighted Rust code
- **Visualizations**: All 5 panel charts embedded

## Customization

### Colors

Edit CSS variables in `css/style.css`:

```css
:root {
    --primary-color: #2563eb;
    --secondary-color: #7c3aed;
    --accent-color: #06b6d4;
    /* ... */
}
```

### Content

- Main content: Edit `index.html`
- Styling: Edit `css/style.css`
- Images: Add to `images/` directory

## Links

All internal links should work when deployed:

- Paper: `/publication/poincare-trajectory-computing.pdf`
- Examples: `/examples/program_synthesis/`
- Documentation: `/RUST_IMPLEMENTATION.md`

## Maintenance

To update visualizations:

```bash
# Regenerate visualizations
cd examples/program_synthesis
python generate_visualizations.py

# Copy to docs
cp visualizations/panel_*.png ../../docs/images/
```

## License

MIT License - see [LICENSE](../LICENSE) for details.
