import { withRouter, useHistory } from 'react-router-dom';

const DashboardContainer = () => {
  const history = useHistory();

  history.push('/upload');

  return null;
};

export default withRouter(DashboardContainer);
