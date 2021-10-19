import React from 'react';

const teamColumns = [{
  accessor: (item) => (`${item.player.team.t_name} (${item.player.team.t_code})`),
  Cell: (item) => {
    const { value } = item;

    return (
      <>
        <span className="d-none d-xl-inline">{value}</span>
      </>
    );
  },
  align: 'left',
  filterBy: 'team',
  Header: 'Name (Code)',
  headerAlign: 'left',
  id: 'team',
  sortBy: ['player__team__t_name', 'player__team__t_code'],
  width: 'auto',
}];

export default teamColumns;
