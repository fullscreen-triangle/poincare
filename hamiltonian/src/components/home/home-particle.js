import Link from "next/link";
import React from "react";
import { LoadingTextAnimation } from "../AnimationText";

export default function HomeDefault({ ActiveIndex, handleOnClick }) {
  return (
    <>
      {/* <!-- HOME --> */}
      <div
        className={
          ActiveIndex === 0
            ? "cavani_tm_section active animated flipInX"
            : "cavani_tm_section active hidden animated flipOutX"
        }
        id="home_"
      >
        <div className="cavani_tm_home">
          <div className="content">
            <h3 className="name">Poincar&eacute; Computing</h3>
            <span className="line"></span>
            <h3 className="job">
              <LoadingTextAnimation />
            </h3>
            <p style={{ maxWidth: "600px", margin: "15px auto 30px", opacity: 0.8, fontSize: "16px", lineHeight: 1.6 }}>
              A fundamental reconceptualization of computation. Navigate to pre-existing solutions instead of simulating forward.
            </p>
            <div className="cavani_tm_button transition_link">
              <Link href="#framework">
                <a onClick={() => handleOnClick(1)}>Explore the Framework</a>
              </Link>
            </div>
          </div>
        </div>
      </div>
      {/* <!-- HOME --> */}
    </>
  );
}
