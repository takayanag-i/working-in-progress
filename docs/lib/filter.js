//===============================================================
// フィルタテーブルの共通変数
//===============================================================
var gTfColList = []; // フィルタを適用する列のリスト
var varOeconomicas = []; // テーブルデータを格納する配列

//===============================================================
// オンロードでテーブル初期設定関数をCALL
//===============================================================
window.onload = function () {
    tFilterInit();
  };
  
  const tFilterInit = () => {
    // テーブルと必要な要素を取得
    const wTABLE = document.querySelector("table");
    if (!wTABLE) return;
  
    const wTH = wTABLE.querySelectorAll("th"); // <th> をすべて取得
    const wTR = wTABLE.querySelectorAll("tbody tr"); // <tbody> の行をすべて取得
  
    // 各列にフィルタボタンを追加
    wTH.forEach((th, colIndex) => {
      const wAddBtn = createFilterButton(colIndex); // ボタン生成
      th.innerHTML += wAddBtn; // ボタンを追加
      gTfColList.push(colIndex); // フィルタ対象列に追加
    });
  
    // 各列のデータを準備
    varOeconomicas = Array.from(wTR).map((tr) => {
      const cells = tr.querySelectorAll("td");
      const rowData = {};
      cells.forEach((cell, index) => {
        rowData[index] = cell.innerText.trim(); // 列インデックスをキーにデータを保存
      });
      return rowData;
    });
  };
  
  const createFilterButton = (colIndex) => {
    // フィルタボタンを生成するHTML
    return `
      <div class="tfArea">
        <svg class="tfImg" id="tsBtn_${colIndex}" style="cursor: pointer;" onclick="tFilterCloseOpen(${colIndex})">
          <path d="M0 0 L9 0 L6 4 L6 8 L3 8 L3 4Z"></path>
        </svg>
        <div class="tfList" id="tfList_${colIndex}" style="display:none">
          ${tFilterCreate(colIndex)}
        </div>
      </div>`;
  };
  
  const tFilterCreate = (argCol) => {
    // 指定列のフィルタリスト作成
    const uniqueValues = Array.from(new Set(varOeconomicas.map((row) => row[argCol] || ""))).sort();
    let rcList = "";
  
    // 「すべて」チェックボックス
    rcList += `
      <div class="tfMeisai">
        <input type="checkbox" id="tfData_ALL_${argCol}" checked onclick="tFilterAllSet(${argCol})">
        <label for="tfData_ALL_${argCol}">(すべて)</label>
      </div>
      <form name="tfForm_${argCol}">`;
  
    // 各値のチェックボックス
    uniqueValues.forEach((value, i) => {
      const wItemId = `tfData_${argCol}_r${i}`;
      rcList += `
        <div class="tfMeisai">
          <input type="checkbox" id="${wItemId}" value="${value}" checked onclick="tFilterClick(${argCol})">
          <label for="${wItemId}">${value || "(空白)"}</label>
        </div>`;
    });
  
    rcList += `</form>`;
  
    // フィルタ用文字入力フィールド
    rcList += `
      <div class="tfInStr">
        <input type="text" placeholder="含む文字抽出" id="tfInStr_${argCol}">
      </div>`;
  
    // OK・Cancel ボタン
    rcList += `
      <div class="tfBtnArea">
        <input type="button" value="OK" onclick="tFilterGo()">
        <input type="button" value="Cancel" onclick="tFilterCancel(${argCol})">
      </div>`;
    return rcList;
  };
  
  const tFilterClick = (argCol) => {
    // フィルタリストのチェックボックスクリック時の処理
    const wForm = document.forms[`tfForm_${argCol}`];
    const wAll = document.getElementById(`tfData_ALL_${argCol}`);
    const checkedCount = Array.from(wForm.elements).filter((el) => el.checked).length;
  
    wAll.checked = checkedCount === wForm.elements.length;
  };
  
  const tFilterAllSet = (argCol) => {
    // 「すべて」のチェックボックスに応じて全てのチェックをON/OFF
    const wForm = document.forms[`tfForm_${argCol}`];
    const isChecked = document.getElementById(`tfData_ALL_${argCol}`).checked;
  
    Array.from(wForm.elements).forEach((el) => {
      if (el.type === "checkbox") el.checked = isChecked;
    });
  };
  
  const tFilterGo = () => {
    // フィルタを適用
    const wTABLE = document.querySelector("table");
    const wTR = wTABLE.querySelectorAll("tbody tr");
  
    // 一旦すべて表示
    wTR.forEach((tr) => (tr.style.display = ""));
  
    gTfColList.forEach((colIndex) => {
      const wAll = document.getElementById(`tfData_ALL_${colIndex}`);
      const wFilterStr = document.getElementById(`tfInStr_${colIndex}`).value.trim();
      const wForm = document.forms[`tfForm_${colIndex}`];
  
      if (!wAll.checked || wFilterStr) {
        const checkedValues = Array.from(wForm.elements)
          .filter((el) => el.checked)
          .map((el) => el.value);
  
        wTR.forEach((tr, rowIndex) => {
          const cellValue = varOeconomicas[rowIndex][colIndex] || "";
          if (!checkedValues.includes(cellValue) && !cellValue.includes(wFilterStr)) {
            tr.style.display = "none";
          }
        });
      }
    });
  };
  
  const tFilterCloseOpen = (argCol) => {
    // フィルタリストの開閉
    gTfColList.forEach((colIndex) => {
      document.getElementById(`tfList_${colIndex}`).style.display = colIndex === argCol ? "block" : "none";
    });
  };
  
  const tFilterCancel = (argCol) => {
    // フィルタリストを閉じる
    tFilterCloseOpen(null);
  };