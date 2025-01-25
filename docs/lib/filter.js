window.onload = function () {
    tFilterInit();
  };
  
  const tFilterInit = () => {
    const wTABLE = document.querySelector("table"); // 最初の<table>を取得
    if (!wTABLE) return; // テーブルがない場合は終了
  
    const wTH = wTABLE.querySelectorAll("th"); // 全ての<th>タグを取得
    const wTR = wTABLE.querySelectorAll("tbody tr"); // tbody内の全ての行を取得
  
    let gTfStartRow = 0; // フィルタ開始行のインデックス
    let gTfColList = []; // フィルタを追加した列を保持するリスト
  
    wTH.forEach((th, colIndex) => {
      // フィルタボタンを<th>に追加
      const wAddBtn = createFilterButton(colIndex);
      th.innerHTML += wAddBtn;
  
      // フィルタ対象列をリストに追加
      gTfColList.push(colIndex);
    });
  
    // --- フィルタ機能をボタンに設定 ---
    gTfColList.forEach((colIndex) => {
      const btn = document.getElementById(`tsBtn_${colIndex}`);
      btn.onclick = () => applyFilter(colIndex, wTR);
    });
  };
  
  const createFilterButton = (colIndex) => {
    // フィルタボタンを生成するHTML
    return `
      <div class="tfArea">
        <svg class="tfImg" id="tsBtn_${colIndex}" style="cursor: pointer;">
          <path d="M0 0 L9 0 L6 4 L6 8 L3 8 L3 4Z"></path>
        </svg>
      </div>`;
  };
  
  const applyFilter = (colIndex, rows) => {
    // フィルタを適用
    const filterValue = prompt("Enter filter value for column " + (colIndex + 1)); // ユーザー入力を取得
    if (!filterValue) return; // 入力が空の場合は終了
  
    rows.forEach((row) => {
      const cell = row.cells[colIndex];
      if (cell && !cell.innerText.includes(filterValue)) {
        row.style.display = "none"; // フィルタに一致しない行を非表示
      } else {
        row.style.display = ""; // 一致する行を表示
      }
    });
  };
  