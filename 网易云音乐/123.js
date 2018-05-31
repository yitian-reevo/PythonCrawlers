NEJ.P = function(DC9t) {
        if (!DC9t || !DC9t.length)
            return null;
        var bbR7K = window;
        for (var a = DC9t.split("."), l = a.length, i = a[0] == "window" ? 1 : 0; i < l; bbR7K = bbR7K[a[i]] = bbR7K[a[i]] || {},
        i++)
            ;
        return bbR7K
    }


c9h = NEJ.P
bb0x = NEJ.O  NEJ.O = {};

k9b = c9h("nej.u")  // == NEJ.P("nej.u")

//判断j9a的对象类型是不是u0x
var EF9w = function(j9a, u0x) {
    try {
        u0x = u0x.toLowerCase();
        if (j9a === null)
            return u0x == "null";
        if (j9a === undefined)
            return u0x == "undefined";
        return bb0x.toString.call(j9a).toLowerCase() == "[object " + u0x + "]"
    } catch (e) {
        return !1
    }
};

//判断j9a是不是一个函数
k9b.gP2x = function(j9a) {
    return EF9w(j9a, "function")
}

// i9b是一个数组， cA0x也是，P0x应该是个默认值，对应一个函数变量
// 这个函数我没完全看懂，但是可以看的出这是一系列对数据的处理，
// 因为输入值是固定的的，所以输出应该是一定的
k9b.bd0x = function(i9b, cA0x, P0x) {
    if (!i9b || !i9b.length || !k9b.gP2x(cA0x))
        return this;
    if (!!i9b.forEach) {  //经过调试后，我们的流程会进入这个if语句
        i9b.forEach(cA0x, P0x); 
        return this
    }
    for (var i = 0, l = i9b.length; i < l; i++)
        cA0x.call(P0x, i9b[i], i, i9b);  
    return this
}

var bui2x=function(cqS5X){
	var m0x=[];
	//具体发生了什么我没看懂
	//不过调式结果显示，这里会根据cqS5X里的每个值，从emj里获取其对应的字符串
	//然后把字符串合并并返回
	k9b.bd0x(cqS5X,function(cqQ4U){ 
			m0x.push(Oa3x.emj[cqQ4U])
		});
	return m0x.join("")
};

Oa3x.md=["色","流感","这边","弱","嘴唇","亲","开心","呲牙","憨笑","猫","皱眉","幽灵","蛋糕","发怒","大哭","兔子","星星","钟情","牵手","公鸡","爱意","禁止","狗","亲亲","叉","礼物","晕","呆","生病","钻石","拜","怒","示爱","汗","小鸡","痛苦","撇嘴","惶恐","口罩","吐舌","心碎","生气","可爱","鬼脸","跳舞","男孩","奸笑","猪","圈","便便","外星","圣诞"]
//这个也是类似于md的字典，它的key就是md里的值，太长了这里不列出来了
Oa3x.emj = {
        "色": "00e0b",
        "流感": "509f6",
        "这边": "259df",
        "弱": "8642d",
        "嘴唇": "bc356",
        "亲": "62901",
        "开心": "477df",
        "呲牙": "22677",
        "憨笑": "ec152",
        "猫": "b5ff6",
        "皱眉": "8ace6",
        "幽灵": "15bb7",
        "蛋糕": "b7251",
        "发怒": "52b3a",
        "大哭": "b17a8",
        "兔子": "76aea",
        "星星": "8a5aa",
        "钟情": "76d2e",
        "牵手": "41762",
        "公鸡": "9ec4e",
        "爱意": "e341f",
        "禁止": "56135",
        "狗": "fccf6",
        "亲亲": "95280",
        "叉": "104e0",
        "礼物": "312ec",
        "晕": "bda92",
        "呆": "557c9",
        "生病": "38701",
        "钻石": "14af6",
        "拜": "c9d05",
        "怒": "c4f7f",
        "示爱": "0c368",
        "汗": "5b7a4",
        "小鸡": "6bee2",
        "痛苦": "55932",
        "撇嘴": "575cc",
        "惶恐": "e10b4",
        "口罩": "24d81",
        "吐舌": "3cfe4",
        "心碎": "875d3",
        "生气": "e8204",
        "可爱": "7b97d",
        "鬼脸": "def52",
        "跳舞": "741d5",
        "男孩": "46b8e",
        "奸笑": "289dc",
        "猪": "6935b",
        "圈": "3ece0",
        "便便": "462db",
        "外星": "0a22b",
        "圣诞": "8e7",
        "流泪": "01000",
        "强": "1",
        "爱心": "0CoJU",
        "女孩": "m6Qyw",
        "惊恐": "8W8ju",
        "大笑": "d"
    };
// 从bui2x -> bd0x => m0x 其实就是一个数组迭代，如果你仔细看Oa3x.emj，
// 它其实是个字典，每个key就是md中的一个值，然后每个key对应了一个value值
// value是一个英文字符串
// 综上，这里的window.asrsea后三个变量都是固定的

var bQC7v=window.asrsea(JSON.stringify(j9a), bui2x(["流泪","强"]), bui2x(Oa3x.md), bui2x(["爱心","女孩","惊恐","大笑"]));

e9f.data=k9b.cE1x({params:bQC7v.encText,encSecKey:bQC7v.encSecKey})


//现在来看window.asrsea 可以看到函数末尾window.asrsea = d
//接着看d，d调用了a，b，c，一个一个看
!function() {
	//返回一个16位的字符串，由字符和数字组成
    function a(a) {
        var d, e, b = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", c = "";
        for (d = 0; a > d; d += 1)
            e = Math.random() * b.length,  //[0，1) * len(b)
            e = Math.floor(e),  //所以e最后是b里面的一个字母
            c += b.charAt(e);
        return c
    }

    //
    function b(a, b) {
        var c = CryptoJS.enc.Utf8.parse(b)
          , d = CryptoJS.enc.Utf8.parse("0102030405060708")
          , e = CryptoJS.enc.Utf8.parse(a)
          , f = CryptoJS.AES.encrypt(e, c, {  //e是text，c是key，iv是12345678，mode是CBC
            iv: d,
            mode: CryptoJS.mode.CBC
        });
        return f.toString()
    }
    function c(a, b, c) {
        var d, e;
        return setMaxDigits(131),
        d = new RSAKeyPair(b,"",c),
        e = encryptedString(d, a)
    }
    function d(d, e, f, g) {
        var h = {}
          , i = a(16);
        return h.encText = b(d, g),
        h.encText = b(h.encText, i),
        h.encSecKey = c(i, e, f),
        h
    }
    function e(a, b, d, e) {
        var f = {};
        return f.encText = c(a + e, b, d),
        f
    }
    window.asrsea = d,
    window.ecnonasr = e
}();

JSON.stringify(j9a)
"{"csrf_token":"e4515cd84baa025c38432652ec58839c"}"
bui2x(["流泪", "强"])
"010001"
bui2x(Oa3x.md)
"00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
bui2x(["爱心", "女孩", "惊恐", "大笑"])
"0CoJUm6Qyw8W8jud"
bQC7v.encText
"rdsRQh/dih7+S/el+oncX22H4xtX9hKUouwpYCLdRlzTzyKoBcurbXnp2BbL2DsZFeAoM1iABcq0rYd0H+hm6mHYBwezc4+LlNRh9V3AaVz1CiAr+ImFp0PcnKxO/wjb"
bQC7v.encSecKey
"89370869c72f77ae033c4968506bbd3d6a5439b8d65cdc302e98444ba3631ecd40dcaed09eaa06ea0c1e62a200c637c8126f2e5e3e3bf9a60cdd5987d03cc44e6254c1330d6127ad735bb1de4807c61790b491c1a4893660e3a4298755581a641fd98ed3857b93b2b06bd5bfb47cb84ec079cdc74ee736fddd1926f97449d5dc"