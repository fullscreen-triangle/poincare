import "particles.js/particles";
import React, { useEffect } from "react";
export default function AuthorDefault() {
  useEffect(() => {
    const particlesJS = window.particlesJS;
    particlesJS.load("particles-js", "particlesConfig.json", function () {
      console.log("hi");
    });
  }, []);

  return (
    <>
      <div className="author_image">
        <div
          className="main"
          style={{
            background: "linear-gradient(135deg, #0a0a2e 0%, #1a1a4e 50%, #0d0d3d 100%)",
          }}
        ></div>
        <div className="particle_wrapper">
          <div id="particles-js" />
        </div>
      </div>
    </>
  );
}
