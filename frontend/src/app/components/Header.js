import React from "react";
import logo from "../styles/images/BCID_H_rgb_rev.png";
import Logout from "./Logout";

const Header = () => {
  return (
    <div className="page-header">
      <div className="cthub-banner">
        <div className="left">
          <a href="https://www.gov.bc.ca" rel="noopener noreferrer">
            <img src={logo} alt="Government of B.C." />
          </a>
          <a href="/upload" rel="noopener noreferrer">
            Clean Transportation DataHub
          </a>
        </div>
        <div className="right">
          <Logout />
        </div>
      </div>
    </div>
  );
};

export default Header;
