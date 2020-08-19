var BACKGROUND
var TABLE
var DATA = []
var CURR_DAY
// I hate that i cant use a dict for this (I need to be able to iterate over keys
// sets of 3 (pixX, pixY, cases)
var LOC_TO_CASES = []
var CURR_IND

function preload() {
  //csv format: date, cases, pixX, pixY
  TABLE = loadTable("clean.csv", "csv", "header")
  BACKGROUND = loadImage("map.png")
}


function setup() {
  createCanvas(BACKGROUND.width, BACKGROUND.height)
  for (let r = 0; r < TABLE.getRowCount(); r++) {
    var currArr = []
    //append date
    currArr[0] = TABLE.getString(r, 0)
    //append cases
    currArr[1] = int(TABLE.getString(r, 1))
    //append pixX
    currArr[2] = int(TABLE.getString(r, 2))
    //append pixY
    currArr[3] = float(TABLE.getString(r, 3))

    //append entire entry to res data
    DATA[r] = currArr
  }
  fill(255, 0, 0); textSize(60);
  CURR_DAY = TABLE.getString(0, 0); CURR_IND = 0;
  frameRate(4)
}

function draw() {
  background(BACKGROUND)

  //get all entries corresponding to only one day
  while (CURR_IND != DATA.length && DATA[CURR_IND][0] == CURR_DAY) {
    let currX = str(DATA[CURR_IND][2])
    let currY = str(DATA[CURR_IND][3])
    let pos = null;

    //find corresponding index for LOC_TO_CASES
    for (let i = 0; i < LOC_TO_CASES.length; i+=3) {
      if (LOC_TO_CASES[i] == currX && LOC_TO_CASES[i+1] == currY) {
        pos = i; break;
      }
    }

    if (!pos) {
     pos = LOC_TO_CASES.length
    }

    LOC_TO_CASES[pos] = currX
    LOC_TO_CASES[pos+1] = currY
    LOC_TO_CASES[pos+2] = DATA[CURR_IND][1]
    CURR_IND++
  }

  for (let i = 0; i < LOC_TO_CASES.length; i+=3) {
    //map size of circles and alpha vals based on how many cases
    let cirSize = map(LOC_TO_CASES[i+2], 1, 500000, 5, 600)
    let alpha = map(LOC_TO_CASES[i+2], 1, 500000, 100, 255)
    fill(255, 0, 0, alpha)
    circle(LOC_TO_CASES[i], LOC_TO_CASES[i+1], cirSize)
  }

  fill(255, 0, 0)
  let dateArr = split(CURR_DAY, '-')
  let dateText = dateArr[1] + '/' + dateArr[2] + '/' + dateArr[0]
  text(dateText, 100, BACKGROUND.height - 200)

  //if weve reached the last entry in dataset, done drawing
  if (CURR_IND == DATA.length) {noLoop(); return;}

  CURR_DAY = DATA[CURR_IND][0]


}
