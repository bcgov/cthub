import React from "react";
import { Route } from "react-router-dom";

import IcbcDataContainer from "./IcbcDataContainer";

const Router = () => [
  <Route exact key="route-icbc" path="/icbc">
    <IcbcDataContainer />
  </Route>,
];

export default Router;
