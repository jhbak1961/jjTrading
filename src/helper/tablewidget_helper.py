# -*- coding: utf-8 -*-

import library.log as LOG

def get_items_selected_rows(tableWidget):
    """TableWidget 의 선택영역에 대한 item 값을 이중 리스트로 전달한다.

        :param tableWidget: table widget object
        :return : list, [[item1,item2,...], ... ]
    """
    # 다중선택모드인 경우 선택된 row의 item 들을 전달한다.
    bind_list = list()
    picks = tableWidget.selectedRanges()

    for picker in picks:
        # LOG.debug(picker.rowCount(), picker.columnCount(), picker.topRow(), picker.bottomRow(),
        #           picker.leftColumn(), picker.rightColumn())
        for row in range(picker.topRow(), picker.bottomRow() + 1):
            items = list()
            for col in range(picker.leftColumn(), picker.rightColumn()):
                items.append(tableWidget.item(row, col).text())

            bind_list.append(items)

    return bind_list


# @TODO : 단일 selecet 항목값 전달 함수를 만들자. 2020.01.16