# -*- coding: utf-8 -*-

import library.log as LOG

def get_items_selected_rows(tableView):
    """TableView  의 선택영역에 대한 item 값을 이중 리스트로 전달한다.

        :param tableView: table widget object
        :return : list, [[item1,item2,...], ... ]
    """
    # TableView (model type) 에서 select 된 모든 row의 항목 가져오는 방법. (다중 선택 모드)
    bind_list = list()
    rows = tableView.selectionModel().selectedRows()
    model = tableView.model()
    LOG.debug(rows, model.columnCount())
    for row in rows :
        items = list()
        for col in range(model.columnCount()):
            items.append(model.data(model.index(row.row(), col)))

        bind_list.append(items)
    return bind_list

def get_item_selected_row(tableView) :
    """TableView  의 선택영역에 대한 item 값을 리스트로 전달한다. (선택된 전체의 데이터 전달, is not sorted)

        :param tableView: table widget object
        :return : list, [item1,item2, ...]
    """
    bind_list = list()
    for idx in tableView.selectedIndexes() :
        LOG.debug(tableView.model().data(idx),
                  idx.row(), idx.column(), idx.data())
        bind_list.append(tableView.model().data(idx))

    return bind_list