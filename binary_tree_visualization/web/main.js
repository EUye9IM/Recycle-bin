// 配置参数
var cfg = {
	initTree: ",A,B,C,D,,E,F,G,H,,,,I",
	cvsw: 1000, // 画布宽
	cvsh: 800,  // 画布高
	nodew: 90,  // 节点间距（宽
	nodeh: 130,  // 节点间距（高
	noder: 40,
	nodeb: 1
};
// 二叉树用数组描述，1 为根节点，2*i 为左子树，2*i+1 为右子树\

var eCvs = document.getElementById("cvs");
var ctx = eCvs.getContext("2d");

var eTreeText = document.getElementById("treetext");
var eTreeOrder = document.getElementById("treeOrder");
var eNodeNum = document.getElementById("nodeNum");
var eLeafNodeNum = document.getElementById("leafNodeNum");
var eTreeDepth = document.getElementById("treeDepth");
var eAnswer = document.getElementById("answer");
var eThreaded = document.getElementById("threaded");

var nodeArray;    // 二叉树数据数组
var nodePos = [];      //节点坐标
var nodeOrder = [0];

var curNode = 0;
var preNode = 0;
var posNode = 0;

var cvsT = {
	sc: 1,
	dx: 0,
	dy: 0
};

function prePosUpdate() {
	if (curNode == 0) {
		preNode = 0;
		posNode = 0;
	} else {
		for (var i = 1; i < nodeOrder.length; i++) {
			if (nodeOrder[i] == curNode) {
				preNode = nodeOrder[i - 1];
				posNode = nodeOrder[i + 1];
				return;
			}
		}
	}
}
function reDrawNode(id, color) {
	if (id == 0 || id == undefined) return;
	ctx.fillStyle = color;
	ctx.beginPath();
	ctx.arc(nodePos[id].x, nodePos[id].y, cfg.noder, 0, 2 * Math.PI);
	ctx.fill();

	ctx.fillStyle = "#000000";
	ctx.font = "40px sans-serif";
	ctx.textAlign = "center";
	ctx.textBaseline = "middle";
	ctx.fillText(nodeArray[id], nodePos[id].x, nodePos[id].y, 1.5 * cfg.noder);
}

function draw() {
	ctx.fillStyle = "#000000";
	eCvs.height = eCvs.height;
	ctx.setTransform(cvsT.sc, 0, 0, cvsT.sc, cvsT.dx, cvsT.dy);
	for (i in nodeArray) {
		if (nodeArray[i] != undefined) {
			if (i != 1) {
				ctx.beginPath();
				ctx.moveTo(nodePos[i].x, nodePos[i].y);
				ctx.lineTo(nodePos[(i - i % 2) / 2].x, nodePos[(i - i % 2) / 2].y)
				ctx.stroke();
			}
		}
	}
	for (i in nodeArray) {
		if (nodeArray[i] != undefined) {
			ctx.fillStyle = "#000000";
			ctx.beginPath();
			ctx.arc(nodePos[i].x, nodePos[i].y, cfg.noder + cfg.nodeb, 0, 2 * Math.PI);
			ctx.fill();
			ctx.fillStyle = "#F0F0F0";
			ctx.beginPath();
			ctx.arc(nodePos[i].x, nodePos[i].y, cfg.noder, 0, 2 * Math.PI);
			ctx.fill();
			ctx.fillStyle = "#000000";
			ctx.font = "40px sans-serif";
			ctx.textAlign = "center";
			ctx.textBaseline = "middle";
			ctx.fillText(nodeArray[i], nodePos[i].x, nodePos[i].y, 1.5 * cfg.noder);
		}
	}

	reDrawNode(curNode, "#e0c0e0");
	reDrawNode(preNode, "#c0c0f0");
	reDrawNode(posNode, "#f0c0c0");
	return;
}
function resetCvs() {
	var dsc = (1 - cvsT.sc) / 50;
	var ddx = (1 - cvsT.dx) / 50;
	var ddy = (1 - cvsT.dy) / 50;
	var interval = setInterval(function () {
		cvsT.sc += dsc;
		cvsT.dx += ddx;
		cvsT.dy += ddy;
		draw();
	}, 10);
	setTimeout(function () {
		clearInterval(interval); cvsT = {
			sc: 1,
			dx: 0,
			dy: 0
		};
		draw();
	}, 500);

	return;
}

function updateNodeData() {
	if (curNode == 0) {
		preNode = 0;
		posNode = 0;
		document.getElementById("nodeData").className = "hidden";
	}
	else {
		prePosUpdate()
		document.getElementById("nodeData").className = "";
		document.getElementById("data").innerText = nodeArray[curNode];
		var threadedDataList = document.getElementsByClassName("threadedData");

		if (eThreaded.checked) {//threaded
			if (nodeArray[curNode * 2] == undefined) {
				document.getElementById("ltag").innerText = "1";
				for (var i = 1; i < nodeOrder.length; i++) {
					if (nodeOrder[i] == curNode) {
						if (nodeOrder[i - 1] == 0 || nodeOrder[i - 1] == undefined)
							document.getElementById("lchild").innerText = "null"
						else
							document.getElementById("lchild").innerText = nodeArray[nodeOrder[i - 1]];
						break;
					}
				}
			}
			else {
				document.getElementById("ltag").innerText = "0";
				document.getElementById("lchild").innerText = nodeArray[curNode * 2];
			}

			if (nodeArray[curNode * 2 + 1] == undefined) {
				document.getElementById("rtag").innerText = "1";
				for (var i = 1; i < nodeOrder.length; i++) {
					if (nodeOrder[i] == curNode) {
						if (nodeOrder[i + 1] == 0 || nodeOrder[i + 1] == undefined)
							document.getElementById("rchild").innerText = "null"
						else
							document.getElementById("rchild").innerText = nodeArray[nodeOrder[i + 1]];
						break;
					}
				}
			}
			else {
				document.getElementById("rtag").innerText = "0";
				document.getElementById("rchild").innerText = nodeArray[curNode * 2 + 1];
			}
			for (i in threadedDataList)
				threadedDataList[i].className = "threadedData";

		} else {//no threaded
			if (nodeArray[curNode * 2] == undefined)
				document.getElementById("lchild").innerText = "null";
			else
				document.getElementById("lchild").innerText = nodeArray[curNode * 2];

			if (nodeArray[curNode * 2 + 1] == undefined)
				document.getElementById("rchild").innerText = "null";
			else
				document.getElementById("rchild").innerText = nodeArray[curNode * 2 + 1];

			for (i in threadedDataList)
				threadedDataList[i].className = "hidden threadedData";

		}
	}
}
// 同时清除画面点选
function flesh_() {
	curNode = 0;
	preNode = 0;
	posNode = 0;
	flesh();
}
function tidyArray() {
	var arrlen = 0;
	for (var i = 0; i < nodeArray.length; i++) {
		if (i == 0) nodeArray[i] = undefined;
		if (nodeArray[i] == "") {
			nodeArray[i] = undefined;
		}
		if (i != 1 && nodeArray[i] != undefined) {
			if (nodeArray[(i - i % 2) / 2] == undefined)
				nodeArray[i] = undefined;
		}
		if (nodeArray[i] != undefined) {
			arrlen = i + 1
		}
	}
	nodeArray.length = arrlen;
	eTreeText.value = nodeArray.toString();
}
function flesh() {
	// 先序遍历
	function preorderTree(tree, root) {
		var ret = "";
		var tmp;
		if (tree[root] != undefined) {
			ret += tree[root];
			nodeOrder.push(root);
			tmp = preorderTree(tree, root * 2);
			if (tmp.length > 0)
				ret += ",";
			ret += tmp;
			tmp = preorderTree(tree, root * 2 + 1);
			if (tmp.length > 0)
				ret += ",";
			ret += tmp;
		}
		return ret;
	}
	// 中序遍历
	function inorderTree(tree, root) {
		var ret = "";
		var tmp;
		if (tree[root] != undefined) {
			tmp = inorderTree(tree, root * 2)
			ret += tmp;
			nodeOrder.push(root);
			if (tmp.length > 0)
				ret += ",";
			ret += tree[root];
			tmp = inorderTree(tree, root * 2 + 1);
			if (tmp.length > 0)
				ret += ",";
			ret += tmp;
		}
		return ret;
	}
	// 后序遍历
	function postorderTree(tree, root) {
		var ret = "";
		var tmp;
		if (tree[root] != undefined) {
			tmp = postorderTree(tree, root * 2);
			ret += tmp;
			nodeOrder.push(root);
			if (tmp.length > 0)
				ret += ",";
			tmp = postorderTree(tree, root * 2 + 1);
			ret += tmp;
			if (tmp.length > 0)
				ret += ",";
			ret += tree[root];
		}
		return ret;
	}

	// 获取节点数据
	nodeArray = eTreeText.value.replace(/\s+/g, "").split(",");
	for (i in nodeArray) {
		if (nodeArray[i] != undefined && nodeArray[i].length == 0)
			nodeArray[i] = undefined;
	}

	// 计算树的统计数字
	eNodeNum.innerText = 0;
	eLeafNodeNum.innerText = 0;
	eTreeDepth.innerText = 0;
	for (i in nodeArray) {
		if (i == 0) nodeArray[i] = undefined;
		if (i != 1 && nodeArray[i] != undefined) {
			if (nodeArray[(i - i % 2) / 2] == undefined)
				nodeArray[i] = undefined;
		}
		if (nodeArray[i] != undefined) {
			eNodeNum.innerText++;
			if ((2 ** eTreeDepth.innerText) <= i)
				eTreeDepth.innerText++;
			if (nodeArray[i * 2] == undefined && nodeArray[i * 2 + 1] == undefined)
				eLeafNodeNum.innerText++;
		}
	}

	// 计算节点在画布上的坐标
	for (var i = 0; i < eTreeDepth.innerText; i++) {
		for (var j = 2 ** i; j < 2 ** (i + 1); j++) {
			if (nodeArray[j] != undefined) {
				if (j == 1) {
					nodePos[j] = {};
					nodePos[j].x = cfg.cvsw / 2//cfg.nodew * ((1 + 2 ** (eTreeDepth.innerText - 1)) / 2);
					nodePos[j].y = cfg.nodeh;
				} else {
					nodePos[j] = {};
					if (j % 2) {
						nodePos[j].x = nodePos[(j - 1) / 2].x + cfg.nodew * (2 ** (eTreeDepth.innerText - i - 1)) / 2;
						nodePos[j].y = nodePos[(j - 1) / 2].y + cfg.nodeh;
					} else {
						nodePos[j].x = nodePos[j / 2].x - cfg.nodew * (2 ** (eTreeDepth.innerText - i - 1)) / 2;
						nodePos[j].y = nodePos[j / 2].y + cfg.nodeh;
					}
				}
			}
		}
	}

	//遍历
	nodeOrder = [0];
	switch (eTreeOrder.value) {
		case "preorder":
			eAnswer.innerText = preorderTree(nodeArray, 1);
			break;
		case "inorder":
			eAnswer.innerText = inorderTree(nodeArray, 1);
			break;
		case "postorder":
			eAnswer.innerText = postorderTree(nodeArray, 1);
			break;
	}
	nodeOrder.push(0);

	updateNodeData();
	draw();
}


// 初始化
function resetData() {
	eTreeText.value = cfg.initTree;
	flesh_();
}
// 点击画布
function cvsClick(e) {
	for (i in nodeArray) {
		if (nodeArray[i] != undefined) {
			ctx.beginPath();
			ctx.arc(nodePos[i].x, nodePos[i].y, cfg.noder, 0, 2 * Math.PI);
			if (ctx.isPointInPath(e.offsetX, e.offsetY)) {
				curNode = i;
				prePosUpdate();
				updateNodeData();
				draw();
				return;
			}
		}
	}
	curNode = 0;
	prePosUpdate();
	updateNodeData();
	draw();
}
function changeCurData() {
	smalltalk
		.prompt("修改当前节点值为", "输入空字符串即为删除节点", nodeArray[curNode], {
			buttons: {
				ok: "确认"
			}
		})
		.then((value) => {
			nodeArray[curNode] = value;
			tidyArray();
			flesh_();
		})
		.catch(() => { });
}
function toPre() {
	curNode = preNode;
	flesh();
}
function toPos() {
	curNode = posNode;
	flesh();
}
function toFa() {
	curNode = (curNode - curNode % 2) / 2;
	flesh();
}
function toLC() {
	curNode = curNode * 2;
	if (nodeArray[curNode] == undefined) {
		smalltalk
			.prompt("新建左子节点值为", "", "", {
				buttons: {
					ok: "确认"
				}
			})
			.then((value) => {
				nodeArray[curNode] = value;
				tidyArray();
				if (nodeArray[curNode] == undefined)
					toFa();
				else
					flesh();
			})
			.catch(() => { });
	} else {
		flesh();
	}
}
function toRC() {
	curNode = curNode * 2 + 1;
	if (nodeArray[curNode] == undefined) {
		smalltalk
			.prompt("新建左子节点值为", "", "", {
				buttons: {
					ok: "确认"
				}
			})
			.then((value) => {
				nodeArray[curNode] = value;
				tidyArray();
				if (nodeArray[curNode] == undefined)
					toFa();
				else
					flesh();
			})
			.catch(() => { });
	} else {
		flesh();
	}
}
///////////////////////////////////////////////////////
resetData();

eCvs.onmousedown = function (e) {
	var x = cvsT.dx - e.offsetX;
	var y = cvsT.dy - e.offsetY;
	var ox = e.offsetX;
	var oy = e.offsetY;

	//按下后可移动
	eCvs.onmousemove = function (e) {
		cvsT.dx = x + e.offsetX;
		cvsT.dy = y + e.offsetY;
		eCvs.onclick = null;
		draw();
	};

	//鼠标抬起清除绑定事件
	eCvs.onmouseleave = function () {
		eCvs.onmousemove = null;
		eCvs.onmouseup = null;
		eCvs.onmouseleave = null;
	};
	eCvs.onmouseup = function (e) {
		if ((ox - e.offsetX) ** 2 + (oy - e.offsetY) ** 2 < 20) {
			cvsClick(e);
		}
		eCvs.onmousemove = null;
		eCvs.onmouseup = null;
		eCvs.onmouseleave = null;
	};
}
eCvs.onwheel = function (e) {
	var x = e.offsetX - cvsT.dx;
	var y = e.offsetY - cvsT.dy;
	var ds = 0.998 ** e.deltaY;
	cvsT.dx -= x * (ds - 1);
	cvsT.dy -= y * (ds - 1);
	cvsT.sc *= ds;
	draw();
}