import React, { useState } from 'react'
import Modal from 'react-modal';
import { SVG_Custom1, SVG_Custom2, SVG_Custom3, SVG_Custom4, SVG_Custom5, SVG_Custom6 } from '../../plugin/svg';
export default function Service({ ActiveIndex }) {

    const [isOpen7, setIsOpen7] = useState(false);
    const [modalContent, setModalContent] = useState({});

    function toggleModalFour() {
        setIsOpen7(!isOpen7);
    }
    const service = [
        {
            svg: <SVG_Custom1 />,
            text: "The computational manifold [0,1]\u00B3 with coordinates (S\u2096, S\u209C, S\u2091) representing knowledge, temporal, and evolution entropy.",
            title: "S-Entropy Space",
            text1: "The S-Entropy Space is a unit cube [0,1]\u00B3 that serves as the computational manifold for Poincar\u00E9 Computing. Every observable state maps to a unique point in this space.",
            text2: "The three coordinates are: S\u2096 \u2208 [0,1] for knowledge entropy (distinguishability of states), S\u209C \u2208 [0,1] for temporal entropy (evolution stage), and S\u2091 \u2208 [0,1] for evolution entropy (stability measure).",
            text3: "This compact representation enables O(log N) navigation \u2014 instead of simulating forward through exponentially many states, we locate the target's coordinates directly in entropy space."
        },
        {
            svg: <SVG_Custom2 />,
            text: "Navigate from observed final states backward through partition hierarchy to reconstruct complete trajectories.",
            title: "Backward Completion",
            text1: "Traditional computing simulates forward: Initial \u2192 Apply Laws \u2192 Iterate \u2192 Final State, with complexity O(n\u00B2 \u00B7 t/\u0394t) for n particles.",
            text2: "Poincar\u00E9 Computing reverses this: Final State (observed) \u2192 Find Penultimate \u2192 Recurse \u2192 Complete Trajectory, with complexity O(log\u2083 M) where M is partition depth.",
            text3: "The key insight: the trajectory already exists in phase space. We don't create it through simulation \u2014 we navigate to its pre-existing coordinates. This yields speedups of ~10\u00B2\u2070\u00D7 for systems with N=10\u2076 states."
        },
        {
            svg: <SVG_Custom3 />,
            text: "For bounded dynamical systems, oscillatory, categorical, and entropic structures are mathematically identical.",
            title: "Triple Equivalence",
            text1: "The Triple Equivalence Theorem is the central result of Poincar\u00E9 Computing. It states that for any bounded system at finite resolution, three mathematical structures are identical.",
            text2: "Oscillatory structure (normal modes with frequencies), categorical structure (partition hierarchy), and entropic structure (information coordinates) are all the same object viewed from different angles.",
            text3: "Consequence: Observation = Computation = Processing. Memory address = Semantic content. Measurement = Coordinate extraction. Knowing any one structure fully determines the other two."
        },
        {
            svg: <SVG_Custom4 />,
            text: "Base-3 addressing system providing natural capacity of 3^M states for partition depth M.",
            title: "Ternary Addressing",
            text1: "The framework uses a base-3 (ternary) addressing scheme that naturally emerges from the partition structure of bounded phase spaces.",
            text2: "Each level of the partition hierarchy has three possible states, giving a total capacity of 3^M for depth M. This is connected to the quantum mechanical structure where partition coordinates map to quantum numbers (n, \u2113, m, s).",
            text3: "The ternary system provides capacity 2n\u00B2 states per principal level \u2014 matching the known structure of atomic shells. Doubling the library size adds only one comparison operation, making the system scale logarithmically."
        },
        {
            svg: <SVG_Custom5 />,
            text: "Universal adapter pattern enabling domain-specific measurements to map into S-entropy coordinates.",
            title: "Observer Abstraction",
            text1: "The Observer is the universal interface between domain-specific measurements and the Poincar\u00E9 computing framework. Any measurement instrument becomes an Observer.",
            text2: "Each Observer defines its measurement modalities, resolution limits, and extraction protocol. Computer vision has 12 modalities. Mass spectrometry has m/z peak extraction. Genomics has the cardinal transformation A\u2192(0,+1), T\u2192(0,-1), G\u2192(+1,0), C\u2192(-1,0).",
            text3: "Through the Observer abstraction, the same backward trajectory completion algorithm works across all domains \u2014 only the measurement front-end changes. The mathematical core remains identical."
        },
        {
            svg: <SVG_Custom6 />,
            text: "Direct correspondence between partition coordinates and quantum numbers (n, \u2113, m, s).",
            title: "Partition Coordinates",
            text1: "Partition coordinates provide the addressing scheme for states in bounded phase space. They directly correspond to quantum numbers in atomic physics.",
            text2: "The principal quantum number n maps to partition depth. The angular momentum \u2113 maps to sub-partition level. The magnetic quantum number m maps to orientation within a level. The spin s maps to binary state within a cell.",
            text3: "This isn't an analogy \u2014 it's a mathematical identity. The partition structure of bounded phase space IS the quantum mechanical structure. This explains why the framework achieves 96.3% accuracy on mass spectrometry with 4,271 compounds using zero free parameters."
        }
    ]
    return (
        <>
            {/* <!-- TECHNOLOGY --> */}
            <div className={ActiveIndex === 7 ? "cavani_tm_section active animated flipInX" : "cavani_tm_section hidden animated flipOutX"} id="news_">
            <div className="section_inner">
                    <div className="cavani_tm_service">
                        <div className="cavani_tm_title">
                            <span>Core Technology</span>
                        </div>
                        <div className="service_list">
                            <ul>
                                {service.map((item, i) => (
                                    <li key={i}>
                                        <div className="list_inner" onClick={toggleModalFour}>
                                            {item.svg}
                                            <h3 className="title" onClick={toggleModalFour}>{item.title}</h3>
                                            <p className="text">{item.text}</p>
                                            <a className="cavani_tm_full_link" href="#" onClick={() => setModalContent(item)} />
                                            <div className="service_hidden_details">
                                                <div className="service_popup_informations">
                                                    <div className="descriptions">
                                                        <p>{item.text1}</p>
                                                        <p>{item.text2}</p>
                                                        <p>{item.text3}</p>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </li>
                                ))}
                            </ul>
                        </div>
                    </div>
                </div>

            </div>
            {/* <!-- TECHNOLOGY --> */}

            {modalContent && (
                <Modal
                    isOpen={isOpen7}
                    onRequestClose={toggleModalFour}
                    contentLabel="My dialog"
                    className="mymodal"
                    overlayClassName="myoverlay"
                    closeTimeoutMS={300}
                    openTimeoutMS={300}
                >
                    <div className="cavani_tm_modalbox opened">
                        <div className="box_inner">
                            <div className="close" onClick={toggleModalFour} >
                                <a href="#"><i className="icon-cancel"></i></a>
                            </div>
                            <div className="description_wrap">
                                <div className="service_popup_informations">
                                    <div className="details">
                                        <h3>{modalContent.title}</h3>
                                    </div>
                                    <div className="descriptions">
                                        <p>{modalContent.text1}</p>
                                        <p>{modalContent.text2}</p>
                                        <p>{modalContent.text3}</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </Modal>
            )}
        </>
    )
}
