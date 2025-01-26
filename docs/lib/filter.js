//===============================================================
//  グローバル定数・変数
//===============================================================
let startRow = 0;
const filterState = {}; // フィルタリストの保存状態
let tableData = [];

//===============================================================
//  オンロードでテーブル初期設定関数をCALL
//===============================================================
window.onload = () => {
  tableData = getTableData();
  console.log(tableData);
  tFilterInit(tableData);
}

const getTableData = () => {
  const table = document.querySelector("table");
  if (!table) {
    console.error("テーブル要素がありません");
    return [];
  }

  const rows = Array.from(table.rows);
  if (rows.length === 0) return [];

  return rows.slice(1).map(row => {
    const cells = Array.from(row.cells);
    const rowData = {};
    cells.forEach((cell, index) => {
      rowData[index] = cell.innerText.trim();
    });
    return rowData;
  });
}

function tFilterInit(oeconomicas) {
  const table = document.querySelector("table");
  const rows = table.rows;
  let addBtn = '';
  tableData = oeconomicas;

  const cells = rows[0].cells;

  for (let j = 0; j < cells.length; j++) {
    startRow = 1;
    addBtn = createFilterButton(j);
    cells[j].appendChild(addBtn);
  }
}

const createFilterButton = (colIndex) => {
  const div = document.createElement('div');
  div.className = 'tfArea';

  const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  svg.classList.add('tfImg');
  svg.id = `tsBtn_${colIndex}`;
  svg.innerHTML = '<path d="M0 0 L9 0 L6 4 L6 8 L3 8 L3 4Z"></path>';
  svg.addEventListener('click', () => {
    tFilterCloseOpen(colIndex);
  });

  const tfList = document.createElement('div');
  tfList.className = 'tfList';
  tfList.id = `tfList_${colIndex}`;
  tfList.style.display = 'none';
  tfList.innerHTML = tFilterCreate(colIndex);

  div.appendChild(svg);
  div.appendChild(tfList);

  return div;
}

function tFilterCreate(argCol) {
  const items = [];
  const uniqueItems = {};
  let dropDown = '';
  let item = '';

  for (let i = 0; i < tableData.length - 1; i++) {
    items[i] = tableData[i+1][argCol]; // todo
  }

  const hasNumeric = items.some(item => item.match(/^[-]?[0-9,.]+$/));
  items.sort(hasNumeric ? sortNumA : sortStrA);


  const wItemId = 'tfData_ALL_' + argCol;
  dropDown += '<div class="tfMeisai">';
  dropDown += '<input type="checkbox" id="' + wItemId + '" checked onclick="tFilterAllSet(' + argCol + ')">';
  dropDown += '<label for="' + wItemId + '">(すべて)</label>';
  dropDown += '</div>';

  dropDown += '<form name="tfForm_' + argCol + '">';

  for (let i = 0; i < items.length; i++) {
    item = trim(items[i]);

    if (!(item in uniqueItems)) {
      const wItemId = 'tfData_' + argCol + '_r' + i;
      dropDown += '<div class="tfMeisai">';
      dropDown += '<input type="checkbox" id="' + wItemId + '" value="' + item + '" checked onclick="tFilterClick(' + argCol + ')">';
      dropDown += '<label for="' + wItemId + '">' + (item == '' ? '(空白)' : item) + '</label>';
      dropDown += '</div>';

      uniqueItems[item] = '1';
    }
  }
  dropDown += '</form>';

  dropDown += '<div class="tfInStr">';
  dropDown += '<input type="text" placeholder="含む文字抽出" id="tfInStr_' + argCol + '">';
  dropDown += '</div>';

  dropDown += '<div class="tfBtnArea">';
  dropDown += '<input type="button" value="OK" onclick="tFilterGo()">';
  dropDown += '<input type="button" value="Cancel" onclick="tFilterCancel(' + argCol + ')">';
  dropDown += '</div>';

  return dropDown;
}

function tFilterClick(argCol) {
  const wForm = document.forms['tfForm_' + argCol];
  let wCntOn = 0;
  let wCntOff = 0;
  const wAll = document.getElementById('tfData_ALL_' + argCol);

  for (let i = 0; i < wForm.elements.length; i++) {
    if (wForm.elements[i].type == 'checkbox') {
      if (wForm.elements[i].checked) {
        wCntOn++;
      } else {
        wCntOff++;
      }
    }
  }

  if ((wCntOn == 0) || (wCntOff == 0)) {
    wAll.checked = true;
    tFilterAllSet(argCol);
  } else {
    wAll.checked = false;
  }
}

function tFilterCancel(argCol) {
  tFilterSave(argCol, 'load');
  tFilterCloseOpen('');
}

function tFilterGo() {
  const table = document.getElementsByTagName("table")[0];
  const rows = table.rows;

  for (let i = 0; i < rows.length; i++) {
    if (rows[i].getAttribute('cmanFilterNone') !== null) {
      rows[i].removeAttribute('cmanFilterNone');
    }
  }

  for (let wCol = 0; wCol < tableData.length; wCol++) {
    const wAll = document.getElementById('tfData_ALL_' + wCol);
    const wItemSave = {};
    const wFilterBtn = document.getElementById('tsBtn_' + wCol);
    const wFilterStr = document.getElementById('tfInStr_' + wCol);
    const wForm = document.forms['tfForm_' + wCol];
    let wVal = '';

    for (let i = 0; i < wForm.elements.length; i++) {
      if (wForm.elements[i].type == 'checkbox') {
        if (wForm.elements[i].checked) {
          wItemSave[wForm.elements[i].value] = 1;
        }
      }
    }

    if ((wAll.checked) && (trim(wFilterStr.value) == '')) {
      wFilterBtn.style.backgroundColor = '';
    } else {
      wFilterBtn.style.backgroundColor = '#ffff00';

      for (let i = startRow; i < rows.length; i++) {
        wVal = trim(tableData[i - 1][wCol]); // todo
        if (!wAll.checked) {
          if (!(wVal in wItemSave)) {
            rows[i].setAttribute('cmanFilterNone', '');
          }
        }

        if (wFilterStr.value != '') {
          const reg = new RegExp(wFilterStr.value);
          if (!wVal.match(reg)) {
            rows[i].setAttribute('cmanFilterNone', '');
          }
        }
      }
    }
  }
  tFilterCloseOpen('');
}

function tFilterSave(argCol, argFunc) {
  const wAllCheck = document.getElementById('tfData_ALL_' + argCol);
  if (argFunc == 'save') {
    filterState[wAllCheck.id] = wAllCheck.checked;
  } else {
    wAllCheck.checked = filterState[wAllCheck.id];
  }

  const wForm = document.forms['tfForm_' + argCol];
  for (let i = 0; i < wForm.elements.length; i++) {
    if (wForm.elements[i].type == 'checkbox') {
      if (argFunc == 'save') {
        filterState[wForm.elements[i].id] = wForm.elements[i].checked;
      } else {
        wForm.elements[i].checked = filterState[wForm.elements[i].id];
      }
    }
  }

  const wStrInput = document.getElementById('tfInStr_' + argCol);
  if (argFunc == 'save') {
    filterState[wStrInput.id] = wStrInput.value;
  } else {
    wStrInput.value = filterState[wStrInput.id];
  }
}

const tFilterCloseOpen = (argCol) => {
  for (let i = 0; i < tableData.length; i++) {
    document.getElementById("tfList_" + i).style.display = 'none';
  }

  if (argCol !== '') {
    document.getElementById("tfList_" + argCol).style.display = '';
    tFilterSave(argCol, 'save');
  }
}

const tFilterAllSet = (argCol) => {
  const wChecked = document.getElementById('tfData_ALL_' + argCol).checked;
  const wForm = document.forms['tfForm_' + argCol];

  for (let i = 0; i < wForm.elements.length; i++) {
    if (wForm.elements[i].type == 'checkbox') {
      wForm.elements[i].checked = wChecked;
    }
  }
}

const  tFilterReset = () => {
  const elements = document.querySelectorAll('.tfArea');
  elements.forEach((element) => {
    element.remove();
  });
}

const sortNumA = (a, b) => {
  a = parseInt(a.replace(/,/g, ''));
  b = parseInt(b.replace(/,/g, ''));
  return a - b;
}

const sortStrA = (a, b) => {
  a = a.toString().toLowerCase();
  b = b.toString().toLowerCase();
  if (a < b) return -1;
  if (a > b) return 1;
  return 0;
}

const trim = (argStr) => {
  let rcStr = argStr;
  rcStr = rcStr.replace(/^[\s\u3000\r\n]+/g, '');
  rcStr = rcStr.replace(/[\s\u3000\r\n]+$/g, '');
  return rcStr;
}
