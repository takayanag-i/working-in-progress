//===============================================================
//  フィルタテーブルの共通変数　設定要！
//===============================================================
let gTfStartRow = 0;
const gTfColList = [];             // ボタンが配置されている列番号
const gTfListSave = {};            // フィルタリストの保存状態
let varOeconomicas = '';
let colObj = {};

//===============================================================
//  オンロードでテーブル初期設定関数をCALL
//===============================================================
window.onload = function() {
  colObj = createColObj();
  console.log(colObj);
  varOeconomicas = tableToVarOeconomicas();
  console.log(varOeconomicas);
  tFilterInit(varOeconomicas);
}

function createColObj() {
  // テーブル要素を取得
  const table = document.getElementsByTagName("table")[0];
  if (!table) {
    console.error("Table element not found.");
    return {};
  }

  const colObj = {};
  const rows = table.rows;

  if (rows.length > 0) {
    const headerCells = rows[0].cells;
    for (let i = 0; i < headerCells.length; i++) {
      colObj[i] = "col" + (i + 1);
    }
  }
  return colObj;
}

function tableToVarOeconomicas() {
  // テーブル要素を取得
  const table = document.getElementsByTagName("table")[0];
  if (!table) {
    console.error("Table element not found.");
    return [];
  }

  const varOeconomicas = [];
  const rows = table.rows;
  const headers = [];

  if (rows.length > 0) {
    const headerCells = rows[0].cells;
    for (let i = 0; i < headerCells.length; i++) {
      headers.push("col" + (i + 1));
    }
  }

  for (let i = 1; i < rows.length; i++) {
    const row = rows[i];
    const cells = row.cells;
    const rowData = {};

    for (let j = 0; j < cells.length; j++) {
      rowData[headers[j]] = cells[j].innerText.trim();
    }

    varOeconomicas.push(rowData);
  }

  return varOeconomicas;
}

function tFilterInit(oeconomicas) {
  const table = document.getElementsByTagName("table")[0];
  const rows = table.rows;
  let addBtn = '';
  varOeconomicas = oeconomicas;

  for (let i = 0; i < rows.length; i++) {
    const cells = table.rows[i].cells;

    for (let j = 0; j < cells.length; j++) {
      gTfStartRow = i + 1;

      addBtn = '<div class="tfArea">';
      addBtn += '<svg class="tfImg" id="tsBtn_' + j + '" onclick="tFilterCloseOpen(' + j + ')"><path d="M0 0 L9 0 L6 4 L6 8 L3 8 L3 4Z"></path></svg>';
      addBtn += '<div class="tfList" id="tfList_' + j + '" style="display:none">';
      addBtn += tFilterCreate(j);
      addBtn += '</div>';
      addBtn += '</div>';
      cells[j].innerHTML += addBtn;

      gTfColList.push(j);
    }

    if (addBtn != '') {
      break;
    }
  }
}

function tFilterCreate(argCol) {
  const wItem = [];
  let wNotNum = 0;
  const wItemSave = {};
  let rcList = '';
  let wVal = '';

  for (let i = gTfStartRow; i < varOeconomicas.length; i++) {
    const j = i - gTfStartRow;
    wItem[j] = varOeconomicas[i][colObj[argCol]];
    if (!wItem[j].match(/^[-]?[0-9,\.]+$/)) {
      wNotNum = 1;
    }
  }

  if (wNotNum == 0) {
    wItem.sort(sortNumA);
  } else {
    wItem.sort(sortStrA);
  }

  const wItemId = 'tfData_ALL_' + argCol;
  rcList += '<div class="tfMeisai">';
  rcList += '<input type="checkbox" id="' + wItemId + '" checked onclick="tFilterAllSet(' + argCol + ')">';
  rcList += '<label for="' + wItemId + '">(すべて)</label>';
  rcList += '</div>';

  rcList += '<form name="tfForm_' + argCol + '">';

  for (let i = 0; i < wItem.length; i++) {
    wVal = trim(wItem[i]);

    if (!(wVal in wItemSave)) {
      const wItemId = 'tfData_' + argCol + '_r' + i;
      rcList += '<div class="tfMeisai">';
      rcList += '<input type="checkbox" id="' + wItemId + '" value="' + wVal + '" checked onclick="tFilterClick(' + argCol + ')">';
      rcList += '<label for="' + wItemId + '">' + (wVal == '' ? '(空白)' : wVal) + '</label>';
      rcList += '</div>';

      wItemSave[wVal] = '1';
    }
  }
  rcList += '</form>';

  rcList += '<div class="tfInStr">';
  rcList += '<input type="text" placeholder="含む文字抽出" id="tfInStr_' + argCol + '">';
  rcList += '</div>';

  rcList += '<div class="tfBtnArea">';
  rcList += '<input type="button" value="OK" onclick="tFilterGo()">';
  rcList += '<input type="button" value="Cancel" onclick="tFilterCancel(' + argCol + ')">';
  rcList += '</div>';

  return rcList;
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

  for (let wColList = 0; wColList < gTfColList.length; wColList++) {
    const wCol = gTfColList[wColList];
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

      for (let i = gTfStartRow; i < rows.length; i++) {
        wVal = trim(varOeconomicas[i - 1][colObj[wCol]]);
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
    gTfListSave[wAllCheck.id] = wAllCheck.checked;
  } else {
    wAllCheck.checked = gTfListSave[wAllCheck.id];
  }

  const wForm = document.forms['tfForm_' + argCol];
  for (let i = 0; i < wForm.elements.length; i++) {
    if (wForm.elements[i].type == 'checkbox') {
      if (argFunc == 'save') {
        gTfListSave[wForm.elements[i].id] = wForm.elements[i].checked;
      } else {
        wForm.elements[i].checked = gTfListSave[wForm.elements[i].id];
      }
    }
  }

  const wStrInput = document.getElementById('tfInStr_' + argCol);
  if (argFunc == 'save') {
    gTfListSave[wStrInput.id] = wStrInput.value;
  } else {
    wStrInput.value = gTfListSave[wStrInput.id];
  }
}

function tFilterCloseOpen(argCol) {
  for (let i = 0; i < gTfColList.length; i++) {
    document.getElementById("tfList_" + gTfColList[i]).style.display = 'none';
  }

  if (argCol !== '') {
    document.getElementById("tfList_" + argCol).style.display = '';
    tFilterSave(argCol, 'save');
  }
}

function tFilterAllSet(argCol) {
  const wChecked = document.getElementById('tfData_ALL_' + argCol).checked;
  const wForm = document.forms['tfForm_' + argCol];

  for (let i = 0; i < wForm.elements.length; i++) {
    if (wForm.elements[i].type == 'checkbox') {
      wForm.elements[i].checked = wChecked;
    }
  }
}

function tFilterReset() {
  const elements = document.querySelectorAll('.tfArea');
  elements.forEach((element) => {
    element.remove();
  });
}

function sortNumA(a, b) {
  a = parseInt(a.replace(/,/g, ''));
  b = parseInt(b.replace(/,/g, ''));
  return a - b;
}

function sortStrA(a, b) {
  a = a.toString().toLowerCase();
  b = b.toString().toLowerCase();
  if (a < b) return -1;
  if (a > b) return 1;
  return 0;
}

function trim(argStr) {
  let rcStr = argStr;
  rcStr = rcStr.replace(/^[ 　\r\n]+/g, '');
  rcStr = rcStr.replace(/[ 　\r\n]+$/g, '');
  return rcStr;
}
