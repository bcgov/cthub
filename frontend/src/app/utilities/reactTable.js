const findSortBy = (columns, id) => {
  let value = id;

  for (let i = 0; i < columns.length; i += 1) {
    const column = columns[i];

    if ('columns' in column) {
      value = findSortBy(column.columns, id);

      if (value !== id) {
        return value;
      }
    } else if (column.id === id && 'sortBy' in column) {
      return column.sortBy;
    }
  }

  return value;
};

const getFilters = (state) => {
  const data = {};

  state.filters.forEach((filter) => {
    data[filter.id] = filter.value;
  });

  return data;
};

const getOrderBy = (state) => {
  const orderBy = [];

  state.sortBy.forEach((arr) => {
    let sortByFields = findSortBy(state.columns, arr.id);

    if (!Array.isArray(sortByFields)) {
      sortByFields = [sortByFields];
    }

    sortByFields.forEach((value) => {
      orderBy.push(`${arr.desc ? '-' : ''}${value}`);
    });
  });

  return orderBy.join(',');
};

export {
  findSortBy, getFilters, getOrderBy,
};
