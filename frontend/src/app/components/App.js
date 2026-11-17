import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import useKeycloak from "../utilities/useKeycloak";
import Login from "./Login";
import Layout from "./Layout";
import { ENABLE_KEYCLOAK } from "../../config";
import { IcbcDataContainer } from "../../icbc_data/IcbcDataContainer";
import { UploadContainer } from "../../uploads/UploadContainer";

const App = () => {
  const keycloak = useKeycloak();

  if (ENABLE_KEYCLOAK && !keycloak.authenticated) {
    const redirectUri = window.location.href;
    return <Login redirectUri={redirectUri} />;
  }
  return (
    <Layout>
      <div className="App">
        <div className="App-body">
          <Router>
            <Routes>
              <Route path="/" element={<UploadContainer />}/>
              <Route path="/icbc" element={<IcbcDataContainer />}/>
              <Route path="/upload" element={<UploadContainer />}/>
            </Routes>
          </Router>
        </div>
      </div>
    </Layout>
  );
};

export default App;
