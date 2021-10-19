const playerColumns = [{
  accessor: (item) => (`${item.player.last_name}, ${item.player.first_name}`),
  filterBy: 'player',
  Header: 'Name',
  headerAlign: 'left',
  id: 'player-name',
  sortBy: ['player__last_name', 'player__first_name'],
  width: 150,
}, {
  accessor: 'player.position',
  align: 'left',
  filterBy: 'player__position',
  Header: 'Pos',
  headerAlign: 'left',
  id: 'player-position',
  sortBy: 'player__position',
  width: 50,
}];

export default playerColumns;
