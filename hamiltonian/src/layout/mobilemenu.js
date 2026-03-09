import React,{useEffect} from 'react'
import { dataImage } from '../plugin/plugin'

export default function Mobilemenu({isToggled, handleOnClick}) {
  useEffect(() => {
    dataImage();
  });
    return (
        <>

            {/* MOBILE MENU */}
            <div className={!isToggled ? "cavani_tm_mobile_menu" :  "cavani_tm_mobile_menu opened"} >
                <div className="inner">
                    <div className="wrapper">
                        <div className="avatar">
                            <div className="image" data-img-url="img/about/1.jpg" />
                        </div>
                        <div className="menu_list">
                            <ul className="transition_link">
                                <li onClick={() => handleOnClick(0)}><a href="#home">Home</a></li>
                                <li onClick={() => handleOnClick(1)}><a href="#framework">Framework</a></li>
                                <li onClick={() => handleOnClick(2)}><a href="#applications">Applications</a></li>
                                <li onClick={() => handleOnClick(7)}><a href="#technology">Technology</a></li>
                                <li onClick={() => handleOnClick(3)}><a href="#research">Research</a></li>
                                <li onClick={() => handleOnClick(4)}><a href="#contact">Contact</a></li>
                            </ul>
                        </div>
                        <div className="social">
                            <ul>
                                <li><a href="https://github.com/fullscreen-triangle/poincare" target="_blank" rel="noopener noreferrer"><img className="svg" src="img/svg/social/github.svg" alt="GitHub" /></a></li>
                            </ul>
                        </div>
                        <div className="copyright">
                            <p>Copyright &copy; 2025 Poincar&eacute; Computing</p>
                        </div>
                    </div>
                </div>
            </div>
            {/* /MOBILE MENU */}


        </>
    )
}
