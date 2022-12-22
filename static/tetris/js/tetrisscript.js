//テーブルの情報を格納
let flowerBox = [];

//ブロックの形状と色
const block = [[0,1,0,0,1,0,0,1,1,1],
               [0,1,0,0,1,0,1,1,0,2],
               [0,1,0,0,1,1,0,1,0,3],
               [0,1,0,0,1,0,0,1,0,4],
               [0,0,0,1,1,0,0,1,1,5],
               [0,0,0,0,1,1,1,1,0,6],
               [0,0,0,0,1,1,0,1,1,7],];

//ブロックの中心からの相対距離[[row],[col]]
const FromCenter = [[-1,-1,-1,0,0,0,1,1,1],[-1,0,1,-1,0,1,-1,0,1]];

//ブロック回転時の位置(半時計,色情報もコピー)
const kaiten = [2,5,8,1,4,7,0,3,6,9];

//結果ランク
const rankselect = [["F","E","D","C","B","A","S","SS",
                    "プロ初段","プロ二段","プロ三段","プロ四段：称号「達人」","プロ五段：称号「名人」","プロ六段：称号「極めし者」",
                    "プロ七段：称号「山王」","プロ八段：称号「海王」","プロ九段：称号「天王」","プロ十段：称号「神の子」",
                    "プロ十一段：称号「SuperAttacker」","プロ十二段：称号「炎帝」","プロ十三段：称号「GODKiller」"],
                    [10,40,50,60,80,100,120,150,
                    170,190,200,210,230,250,
                    300,320,340,400,
                    500,700,1000]];

//ブロック中心位置
let centerpoint;

//ブロックの種類(block[]をスライス)
let blocknumber = [];

//落下ブロック数カウンター
let blockcounter;

//ループ停止用
let looperid;




/////画面ロード時/////
window.onload = function() {
    //テーブル初期化
    tablecreate();

    window.addEventListener('keydown', keyDown, true);

    alert("＜＜＜操作説明＞＞＞\n■移動：上下左右キー\n■回転：スペースキー");
}


/////テーブル・変数初期化処理/////
function tablecreate() {
    for (let i = 1; i < 24; i++) {
        $(".tetris_table").append("<tr></tr>");
    }
    for (let i = 1; i < 14; i++) {
        $(".tetris_table tr").append("<td></td>");
    }

    $(".tetris_table tr").eq(4).addClass("goal");

}


/////flower初期化処理/////
function flowerinit() {
    for (let r = 0; r < 25; r++) {
        flowerBox[r] = [];
        for (let c = 0; c < 15; c++) {
            if ( r == 0 || c == 0 || r == 24 || c == 14 ) {
                flowerBox[r][c] = 77;
            }else{
                flowerBox[r][c] = 0;
            }
        }
    }
}


/////STARTボタン押下時/////
function start() {
    //変数初期化
    flowerBox = [];
    flowerinit();
    centerpoint = [3,7];
    blockcounter = 0;
    count = 0;
    NextBlock = true;
    speed = 14;
    looperid = null;

    //結果表示を削除
    $(".kekka").removeClass("kekkahyouzi");

    //ループ開始
    looperid = requestAnimationFrame(mainLoop);

}



//////////////////////////////////////////////
//              メインループ処理             //
/////////////////////////////////////////////

let count = 0;           //ループの合計回数
let kettei = 1;          //ブロック落下中 1 , ブロック落下完了　100
let NextBlock;    //次のブロックを発生させるかさせないか
let speed = 14;          //ブロックの落下スピード　低い方がはやい

function mainLoop() {

    count++;

    //ブロック発生処理
    if ( NextBlock ) {
        RandBlock();
        centerpoint = [3,7];
        NextBlock = false;
        kettei = 1;
        blockcounter++;
        //ブロック5個ごとに落下速度をあげる
        if ( blockcounter % 5 == 0) {
            if (speed > 6) {
                speed--;
            }
        }
    }

    //ブロック落下処理
    if ( count % speed == 0) {
        FlowerErase();
        if ( !centerchange("under") ) {
            NextBlock = true;
            kettei = 100;
        }
        FlowerChange(kettei);
    }

    //揃い列削除処理
    UnderErase();

    //テーブルを更新
    FlowerToTable();

    //ゲームオーバー
    for (let c = 1; c < 14; c++) {
        if (flowerBox[4][c] >= 100) {
            cancelAnimationFrame(looperid);
            KEKKA();
            testtanaka(blockcounter);
            return;
        }
    }

    looperid = requestAnimationFrame(mainLoop);

}



/////キー入力受け取り/////
function keyDown(event) {
    var code = event.keyCode;

    switch(code) {
        case 39:
            FlowerErase();
            centerchange("right");
            FlowerChange(kettei);
            FlowerToTable();
            break;
        
        case 37:
            FlowerErase();
            centerchange("left");
            FlowerChange(kettei);
            FlowerToTable();
            break;

        case 40:
            FlowerErase();
            if ( !centerchange("under") ) {
                NextBlock = true;
                kettei = 100;
            }
            FlowerChange(kettei);
            FlowerToTable();
            break;
        
        case 32:
            FlowerErase();
            KAITEN();
            FlowerChange(kettei);
            FlowerToTable();
            break;
        
    }
}


/////ブロックナンバーの設定/////
function RandBlock() {
    let number
    let math = block.length;
    number = Math.floor( Math.random() * math );
    blocknumber = block[number];
}


/////Flowerをテーブルに転写/////
function FlowerToTable() {
    for (let r = 0; r < 25; r++) {
        for (let c = 0; c < 15; c++) {
            let setrow = r - 1;
            let setcol = c - 1;
            if (flowerBox[r][c] == 1 || flowerBox[r][c] == 100) {
                $(".tetris_table tr").eq(setrow).children().eq(setcol).removeClass().addClass("red");
            }
            if (flowerBox[r][c] == 2 || flowerBox[r][c] == 200) {
                $(".tetris_table tr").eq(setrow).children().eq(setcol).removeClass().addClass("blue");
            }
            if (flowerBox[r][c] == 3 || flowerBox[r][c] == 300) {
                $(".tetris_table tr").eq(setrow).children().eq(setcol).removeClass().addClass("green");
            }
            if (flowerBox[r][c] == 4 || flowerBox[r][c] == 400) {
                $(".tetris_table tr").eq(setrow).children().eq(setcol).removeClass().addClass("orange");
            }
            if (flowerBox[r][c] == 5 || flowerBox[r][c] == 500) {
                $(".tetris_table tr").eq(setrow).children().eq(setcol).removeClass().addClass("yellow");
            }
            if (flowerBox[r][c] == 6 || flowerBox[r][c] == 600) {
                $(".tetris_table tr").eq(setrow).children().eq(setcol).removeClass().addClass("pink");
            }
            if (flowerBox[r][c] == 7 || flowerBox[r][c] == 700) {
                $(".tetris_table tr").eq(setrow).children().eq(setcol).removeClass().addClass("brown");
            }
            if (flowerBox[r][c] == 0) {
                $(".tetris_table tr").eq(setrow).children().eq(setcol).removeClass();
            }
        }
    }
}


/////Flowerの更新（ブロック移動）/////
function FlowerChange(kakeru) {
    for (let i = 0; i < 9; i++) {
        if (blocknumber[i] == 1) {
            let row = centerpoint[0] + FromCenter[0][i];
            let col = centerpoint[1] + FromCenter[1][i];
            flowerBox[row][col] = blocknumber[9] * kakeru;
        }
    }
}


/////Flowerの更新（ブロック削除）/////
function FlowerErase() {
    for (let r = 1; r < 24; r++) {
        for (let c = 1; c < 14; c++) {
            if (flowerBox[r][c] < 50) {
                flowerBox[r][c] = 0;
            }
        }
    }
}


/////centerpointの移動（移動可否確認込み）/////
function centerchange(way) {
    let plusoner = 0;
    let plusonec = 0;
    if (way == "under") {
        plusoner = 1;
    }else if (way == "right") {
        plusonec = 1;
    }else if (way == "left") {
        plusonec = -1;
    }

    for (let b = 0; b < 9; b++) {
        if (blocknumber[b] == 1) {
            let row = centerpoint[0] + FromCenter[0][b] + plusoner;
            let col = centerpoint[1] + FromCenter[1][b] + plusonec;
            if (flowerBox[row][col] != 0 && flowerBox[row][col] != blocknumber[9]) {
                return false;
            }
        }
    }
    centerpoint[0] = centerpoint[0] + plusoner;
    centerpoint[1] = centerpoint[1] + plusonec;
    return true;
}


/////blocknumberの回転（回転可否確認込み）/////  まだ修正できそう
function KAITEN() {
    let blockcopy = [];
    blockcopy = blocknumber.slice();

    for (let n = 0; n < 10; n++) {
        blocknumber[n] = blockcopy[kaiten[n]];
    }

    for (let b = 0; b < 9; b++) {
        if (blocknumber[b] == 1) {
            let row = centerpoint[0] + FromCenter[0][b];
            let col = centerpoint[1] + FromCenter[1][b];
            if (flowerBox[row][col] != 0 && flowerBox[row][col] != blocknumber[9]) {
                blocknumber = blockcopy.slice();
                return false;
            }
        }
    }
}


/////Flowerの更新（揃い行の削除）/////
function UnderErase() {
    let eraseCAN = [];
    let eraser = false;

    for (let r = 1; r < 24; r++) {
        for (let c = 1; c < 14; c++) {
            if (flowerBox[r][c] >= 100) {
                if (c == 13) {
                    eraseCAN[eraseCAN.length] = r;
                    eraser = true;
                }
            }else{
                break;
            }
        }
    }

    if (eraser) {
        for (let can = 0; can < eraseCAN.length; can++) {
            for (let num = eraseCAN[can]; num > 2; num --) {
                flowerBox[num] = flowerBox[num - 1].slice();
            }
            flowerBox[1] = [77,0,0,0,0,0,0,0,0,0,0,0,0,0,77];
        }
    }
}


/////結果表示処理/////
function KEKKA() {
    $(".kekka").addClass("kekkahyouzi");

    let blockcounttext = "count:" + blockcounter + "blocks";        //count:57blocks
    let ranktext;
    let rank;

    for (let i = 0; i < rankselect[0].length; i++) {
        if ( blockcounter < rankselect[1][i]) {
            rank = rankselect[0][i];
            break;
        }
    }

    if (rank == "") {
        rank = "テトリスの神様"
    }

    ranktext = "rank:" + rank;                      //rank:B

    $(".blockcount").text(blockcounttext);
    $(".tetrisrank").text(ranktext);


    // -------about rank-------
    // ~ 10blocks : F
    // ~ 40blocks : E
    // ~ 50blocks : D
    // ~ 60blocks : C
    // ~ 80blocks : B
    // ~ 100blocks : A
    // ~ 120blocks : S
    // ~ 150blocks : SS
    // 151blocks ~ : secret


}