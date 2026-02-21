'use strict';
/* global monogatari */

monogatari.assets('scenes', {
  "aoba_academy_gate": "aoba_academy_gate/background.png",
  "old_library_corner": "old_library_corner/background.png",
  "faculty_office": "faculty_office/background.png",
  "hostile_classroom": "hostile_classroom/background.png",
  "library_strategy_room": "library_strategy_room/background.png",
  "classroom_revenge_site": "classroom_revenge_site/background.png",
  "dusk_library_confrontation": "dusk_library_confrontation/background.png",
  "sealed_school_gate": "sealed_school_gate/background.png",
  "rebirth_library": "rebirth_library/background.png",
  "withered_hospital_room": "withered_hospital_room/background.png",
  "dark_supernatural_library": "dark_supernatural_library/background.png"
});

monogatari.characters({
  "hanako": {
    "name": "花子",
    "color": "#ffffff",
    "directory": "hanako",
    "sprites": {
      "normal": "normal.png",
      "happy": "happy.png",
      "sad": "sad.png",
      "angry": "angry.png",
      "surprised": "surprised.png"
    }
  },
  "yoshiki": {
    "name": "佳樹",
    "color": "#ffffff",
    "directory": "yoshiki",
    "sprites": {
      "normal": "normal.png",
      "happy": "happy.png",
      "sad": "sad.png",
      "angry": "angry.png",
      "surprised": "surprised.png"
    }
  },
  "daiki": {
    "name": "大樹",
    "color": "#ffffff",
    "directory": "daiki",
    "sprites": {
      "normal": "normal.png",
      "happy": "happy.png",
      "sad": "sad.png",
      "angry": "angry.png",
      "surprised": "surprised.png"
    }
  }
});

monogatari.script({
	'Start': [
		'show scene aoba_academy_gate with fadeIn',
		'show character hanako normal at center with fadeIn',
		'東京的春天帶著一種喧囂的冷漠。花子拖著沉重的行李箱站在私立青葉學園的門口，抬頭仰望這座高聳入雲、如同監獄般華美的校舍。',
		'她是從山梨縣的鄉下轉學來的，父母離婚後各自追求夢想，卻都給了她相同的承諾：「妳放心，我們都愛妳。」這句話如今聽來卻無比諷刺。',
		'校長是她父親的兒時好友，特意安排她進入這所名門學校，但父親不知道的是，當年他曾經霸凌過這位校長。這份隱藏的惡意，正悄悄在校園的陰影中發酵。',
		'花子握緊拳頭，對自己說：「我一定不能給爸爸媽媽添麻煩。」然而，入學第一天，現實就擊碎了她的幻想。',
		'抽屜裡的垃圾、被藏起來的室內鞋、倒進水池的書包……惡意的潮水瞬間淹沒了她。今天，她的課本又被丟進了廁所，面對空蕩蕩的課桌，花子感覺自己的呼吸快要停滯了。',
		{
    "Choice": {
        "躲進圖書館哭泣": {
            "Text": "躲進圖書館哭泣",
            "Do": "jump Route_Library"
        },
        "試圖向老師告狀": {
            "Text": "試圖向老師告狀",
            "Do": "jump Route_Teacher"
        },
        "在教室大聲質問是誰做的": {
            "Text": "在教室大聲質問是誰做的",
            "Do": "jump Route_Confront"
        }
    }
}
	],

	'Route_Library': [
		'show scene old_library_corner with fadeIn',
		'show character hanako normal at center with fadeIn',
		'花子選擇了逃跑，她一路穿過長廊，躲進了校園最偏僻的圖書館角落。這裡空氣中瀰漫著古舊書卷的氣息，讓她的恐懼稍微平復。',
		'她縮在書架後的陰影裡，眼淚止不住地掉下來，浸濕了裙襬。就在這時，她面前的一本書竟無風自鼓，頁面快速翻動。',
		'一個清冷且帶著一絲慵懶的男聲從背後傳來：「那本不適合妳，那是一本關於自我毀滅的詩集。」花子嚇得跌坐在地，回頭看見一個穿著舊式校服、半透明的男生站在窗邊。',
		'show character hanako normal at left',
		'show character yoshiki normal at right with fadeIn',
		'他是佳樹，這座圖書館的幽靈。佳樹看著花子哭腫的雙眼，語氣中帶著一絲同情：「妳跟我當年很像，只是我選擇了跳下去。',
		'想反擊嗎？我可以教妳，但妳得先學會信任我這個死人。',
		'」這種在最絕望時遇見的陪伴，讓花子心中生出了一絲異樣的依賴感。',
		{
    "Choice": {
        "繼續": {
            "Text": "繼續",
            "Do": "jump Meet_Yoshiki"
        }
    }
}
	],

	'Route_Teacher': [
		'show scene faculty_office with fadeIn',
		'show character hanako normal at center with fadeIn',
		'花子敲開了教職員室的大門，鼓起勇氣向導師訴說這幾天的遭遇。然而，老師甚至沒有抬頭看她一眼，只是機械式地翻動著文件，冷淡地說：「花子同學，大家只是在跟妳開玩笑，妳太敏感了。',
		'身為轉學生，妳應該主動融入班級，而不是來這裡打小報告。妳知道這會影響班級榮譽評分嗎？',
		'」這番話如同冰水潑下，讓花子徹底絕望。原來在這個權力的象徵地，真相並不重要。',
		'show character hanako normal at left',
		'show character yoshiki normal at right with fadeIn',
		'她失魂落魄地走進圖書館，試圖尋找一點安寧。就在她盯著手中的課本殘骸發呆時，佳樹出現了。',
		'他冷笑著看著花子：「老師是救不了妳的，他們只在乎那層薄薄的皮。想變得激進一點嗎？',
		'我可以教妳如何讓他們感到真正的恐懼。」花子的心在那一刻變得堅硬起來，仇恨取代了悲傷。',
		{
    "Choice": {
        "繼續": {
            "Text": "繼續",
            "Do": "jump Meet_Yoshiki"
        }
    }
}
	],

	'Route_Confront': [
		'show scene hostile_classroom with fadeIn',
		'show character hanako normal at center with fadeIn',
		'花子沒有退縮，她用力一拍桌子，轉過身對著滿教室的同學大聲質問：「這到底是誰做的？出來跟我當面對質！',
		'」教室瞬間陷入死寂，隨後爆發出更劇烈的嘲笑聲。霸凌的首領推了她一把，譏諷道：「鄉下來的野豬妹生氣囉？',
		'show character hanako normal at left',
		'show character yoshiki normal at right with fadeIn',
		'真可怕啊！」雖然被羞辱，但花子眼神中的那股倔強卻引起了在暗處觀察的佳樹的興趣。',
		'當花子疲憊地躲進圖書館喘息時，佳樹直接顯現在她面前。他鼓起掌來，雖然發不出聲音：「真有勇氣，很久沒見過這麼有趣的傢伙了。',
		'妳的勇氣很珍貴，但缺乏謀略。光有怒火是不夠的，妳需要的是讓他們閉嘴的力量。',
		'」因為花子展現出的韌性，佳樹對她的指導顯得更加主動且具備戰術性，兩人之間形成了一種類似戰友的關係。',
		{
    "Choice": {
        "繼續": {
            "Text": "繼續",
            "Do": "jump Meet_Yoshiki"
        }
    }
}
	],

	'Meet_Yoshiki': [
		'show scene library_strategy_room with fadeIn',
		'show character yoshiki normal at left with fadeIn',
		'show character hanako normal at right with fadeIn',
		'佳樹告訴花子，他當年是因為被推下樓才變成幽靈的，而那些兇手現在依然在校園某處逍遙法外。他教導花子：「不用努力去當風雲人物，也不要追隨那些虛偽的時尚。',
		'別人要欺負妳，不管妳多完美，他們總能找到藉口。妳首先要強大心理，再來要有實際作為。',
		'」在圖書館的秘密時光裡，佳樹傳授她心理戰術：如何觀察對方的弱點、如何利用流言分化霸凌團體。花子發現佳樹雖然是鬼，卻比任何人都看得清人性。',
		'然而，隨著兩人接觸的增加，花子開始頻繁頭暈，甚至流鼻血，她沒意識到與靈魂過度接觸正在消耗她的生命力。佳樹看著她日漸蒼白的臉孔，欲言又止。',
		'終於，班上的欺凌升級到了頂點，他們在午休時將花子圍在角落，剪去了她的頭髮並拍照取笑。這一次，花子決定按照佳樹的計畫進行大反擊。',
		{
    "Choice": {
        "威脅要與對方同歸於盡": {
            "Text": "威脅要與對方同歸於盡",
            "Do": "jump Route_Threaten"
        },
        "冷靜地將水潑向自己，笑著看著他們": {
            "Text": "冷靜地將水潑向自己，笑著看著他們",
            "Do": "jump Route_Cold"
        }
    }
}
	],

	'Route_Threaten': [
		'show scene classroom_revenge_site with fadeIn',
		'show character hanako normal at center with fadeIn',
		'花子猛地站起來，手裡提著一桶從實驗室拿來的「透明液體」（其實只是加了味道的水）。她眼神瘋狂地掃視全班，冷冷地說：「妳們知道嗎？',
		'我是未成年，妳們也是。妳們逼死我不用判刑，但我拉著妳們一起走，法律也奈何不了我。',
		'要下地獄，大家一起去吧！」說完，她將桶子重重摔在地上，液體濺濕了那些霸凌者的鞋子。',
		'show character hanako normal at left',
		'show character yoshiki normal at right with fadeIn',
		'全班瞬間安靜得連針掉在地上都能聽見，霸凌者們尖叫著退後，被她眼中那種毀滅性的氣息徹底震懾住。佳樹在旁邊露出滿意的微笑。',
		'雖然這暫時止住了霸凌，但校園裡開始流傳「花子瘋了」的謠言，這種不穩定的形象讓她之後的處境變得更加詭譎，但也換來了短暫的平靜。花子的心在這一刻變得比以前冷硬了許多。',
		{
    "Choice": {
        "繼續": {
            "Text": "繼續",
            "Do": "jump Daiki_Interaction"
        }
    }
}
	],

	'Route_Cold': [
		'show scene hostile_classroom with fadeIn',
		'show character hanako normal at center with fadeIn',
		'花子沒有大吼大叫，反而接過霸凌者手中的水桶，緩緩地從自己頭上澆了下去。她在全班驚愕的注視下，露出一種令人毛骨悚然的甜美笑容，一邊抹掉臉上的水一邊輕聲說：「這樣滿意了嗎？',
		'如果不夠，我可以多淋一點。反正這副身體已經壞掉了，你們想看看壞掉的東西裡面裝什麼嗎？',
		'show character hanako normal at left',
		'show character yoshiki normal at right with fadeIn',
		'」那種極度不正常的神經特質讓周圍的人感到一陣寒意，霸凌者們面面相覷，原本的優越感變成了恐懼，紛紛找藉口離開教室。佳樹看著花子，輕聲嘆道：「這招比我想像的還要狠毒，妳在利用自己的痛苦來製造他們的心理陰影。',
		'」從此之後，雖然沒人敢直接動手，但全班陷入了長期的精神冷戰。花子在那種詭異的靜默中，感覺自己正慢慢遠離人類的世界。',
		{
    "Choice": {
        "繼續": {
            "Text": "繼續",
            "Do": "jump Daiki_Interaction"
        }
    }
}
	],

	'Daiki_Interaction': [
		'show scene library_strategy_room with fadeIn',
		'show character daiki normal at left with fadeIn',
		'show character yoshiki normal at right with fadeIn',
		'就在校園局勢緊繃時，一名叫「大樹」的實習老師來到了學校。他其實是佳樹的親哥哥，改名換姓就是為了調查弟弟的真正死因。',
		'show character hanako normal at center with fadeIn',
		'他注意到花子經常獨自待在圖書館，且言行舉止中隱約有弟弟當年的影子。某天放學，大樹在圖書館角落攔住了花子，眼神中充滿了痛苦與渴望：「花子同學，我知道妳在那裡。',
		'我看過那些紀錄，妳現在的情況和佳樹當年一模一樣。告訴我，他當初到底是怎麼死的？',
		'是他們……推他下去的，對嗎？」佳樹此時正站在大樹身後，透明的手試圖觸碰哥哥卻只是穿透而過。',
		'佳樹在花子耳邊低語：「別告訴他真相，我不想讓他背負殺人的罪惡活下去，這會毀了他的前途。」花子看著大樹憔悴的臉龐，陷入了掙扎。',
		{
    "Choice": {
        "告訴他真相：佳樹是被推下去的": {
            "Text": "告訴他真相：佳樹是被推下去的",
            "Do": "jump Route_Truth"
        },
        "守住秘密：安慰大樹這只是意外": {
            "Text": "守住秘密：安慰大樹這只是意外",
            "Do": "jump Route_Secret"
        }
    }
}
	],

	'Route_Truth': [
		'show scene dusk_library_confrontation with fadeIn',
		'show character hanako normal at center with fadeIn',
		'「他是被推下去的，那些人依然在笑著。」花子最終選擇了說出真相。',
		'show character hanako normal at left',
		'show character daiki normal at right with fadeIn',
		'大樹的眼神在那一刻從悲傷轉為極度的狂怒與毀滅慾。他握緊拳頭，聲音顫抖著感謝花子，隨即開始了私下的調查與報復行動。',
		'show character yoshiki normal at center with fadeIn',
		'佳樹看著哥哥陷入仇恨的深淵，靈魂劇烈動搖，散發出的黑影幾乎蓋過了圖書館的燈光。大樹利用教師的權限，開始威脅並誘使當年的兇手露出馬腳，校園氛圍變得如同驚悚懸疑劇。',
		'花子發現自己捲入了一場停不下來的復仇風暴中。雖然正義似乎在伸張，但她也看到大樹漸漸失去了原本的溫柔，變得和霸凌者一樣殘忍。',
		'佳樹看著這一切，絕望地閉上雙眼：「小花，這不是我想看到的，真相有時候比謊言更致命。」花子的身體狀況加速惡化，她感到死亡正步步逼近。',
		{
    "Choice": {
        "繼續": {
            "Text": "繼續",
            "Do": "jump Final_Decision"
        }
    }
}
	],

	'Route_Secret': [
		'show scene rebirth_library with fadeIn',
		'show character daiki normal at left with fadeIn',
		'show character yoshiki normal at right with fadeIn',
		'show character hanako normal at center with fadeIn',
		'「老師，那真的只是一場意外。」花子看著大樹的眼睛，忍痛撒了謊，「佳樹當時只是太累了，他並沒有恨任何人，他希望你能好好活下去。',
		'」聽到這番話，大樹緊繃的肩膀終於跨了下來，在空蕩蕩的圖書館裡掩面痛哭。佳樹在後方輕輕點頭，向花子露出感激的神情。',
		'雖然大樹不再尋求報復，回歸了平靜的生活，但這意味著當年的罪惡將永遠沉入水底。花子必須獨自承擔這個秘密，以及與幽靈合作所帶來的代價。',
		'她的生命力依舊在流逝，因為佳樹對她的依戀與保護成為了一種無形的詛咒。霸凌者們因為花子的沉默而逃過一劫，但花子已經學會了如何在那種環境中守護自己。',
		'她和佳樹之間的關係變得更加深厚且沉重，彷彿兩個人共用著一個逐漸凋零的靈魂。',
		{
    "Choice": {
        "繼續": {
            "Text": "繼續",
            "Do": "jump Final_Decision"
        }
    }
}
	],

	'Final_Decision': [
		'show scene dark_supernatural_library with fadeIn',
		'show character hanako normal at center with fadeIn',
		'最後的危機來臨了。霸凌者們為了徹底除掉「邪門」的花子，在校門口貼滿了從神社求來的強力符咒。',
		'show character hanako normal at left',
		'show character yoshiki normal at right with fadeIn',
		'這些符咒形成了封印結界，佳樹的力量被大幅削弱，甚至開始感受到靈魂被撕裂的痛苦。而花子因為長期的能量消耗，已經虛弱到連走路都困難。',
		'佳樹看著花子，用盡最後的力量顯形：「小花，這是最後的機會。人鬼不能長久共處，我的存在只會拖垮妳。',
		'那些符咒雖然是封印，但只要妳親手撕下它，這股能量的爆發會讓我被強制送入輪迴，而妳也會恢復健康。如果不這樣做，妳會死，而我會永遠被卡在這裡。',
		'或者是……妳可以利用我最後的怨恨，將那些符咒的能量逆轉，讓那些人付出代價。」花子顫抖著手，站在校門口的符咒前。',
		{
    "Choice": {
        "聽從佳樹，撕下符咒（自我救贖）": {
            "Text": "聽從佳樹，撕下符咒（自我救贖）",
            "Do": "jump Ending_Redemption"
        },
        "保留符咒，試圖尋找共存的方法（淒美悲劇）": {
            "Text": "保留符咒，試圖尋找共存的方法（淒美悲劇）",
            "Do": "jump Ending_Tragedy"
        },
        "利用符咒的力量將霸凌者拉入深淵（黑化）": {
            "Text": "利用符咒的力量將霸凌者拉入深淵（黑化）",
            "Do": "jump Ending_Abyss"
        }
    }
}
	],

	'Ending_Redemption': [
		'show scene aoba_academy_gate with fadeIn',
		'show character hanako normal at center with fadeIn',
		'花子用盡全力撕下了校門口的符咒。一瞬間，柔和的白光包圍了整個圖書館。',
		'show character hanako normal at left',
		'show character yoshiki normal at right with fadeIn',
		'佳樹的身影漸漸碎裂成光點，他露出了解脫的笑容：「小花，不要靠鬼，妳還活著，活著的人比鬼更有力量。」隨著連結的斷開，花子的頭痛和虛弱瞬間消失。',
		'佳樹徹底消失在輪迴的彼岸，留下的是花子對生命的新理解。幾個月後，花子依然在青葉學園就讀，她不再是那個唯唯諾諾的女孩，即使面對冷言冷語，她也能帶著佳樹教她的智慧堅強應對。',
		'她送走了幽靈，卻迎來了真正的自己。在陽光灑落的圖書館裡，她翻開一本書，彷彿還能聽見那句慵懶的：『這本不適合妳』。',
		'她知道，她會帶著這份勇氣一直走下去。',
		'centered ── 結局：Redemption ──',
		'end'
	],

	'Ending_Tragedy': [
		'show scene withered_hospital_room with fadeIn',
		'show character hanako normal at center with fadeIn',
		'花子緊緊抱住那些符咒，不肯動手。「我不要失去你！',
		'show character hanako normal at left',
		'show character yoshiki normal at right with fadeIn',
		'」她哭喊著。她選擇了保留符咒，試圖尋找能讓佳樹留下來的方法。',
		'然而，命運是殘酷的，違背自然規則的代價很快找上了她。花子的生命力被無止盡地抽取，她的身體一天天衰弱下去，最終不得不退學住進醫院。',
		'佳樹被迫與花子綑綁在一起，他只能站在病床邊，看著這個曾經活潑的少女在無盡的悔恨中慢慢枯萎。兩人都無法獲得解脫，佳樹後悔幫了她，而花子在失去意識前，手依然在虛空中抓著什麼。',
		'圖書館裡再也沒有了那對談論心理學的人影，只剩下一個逐漸消散的靈魂和一個再也無法醒來的女孩，在永恆的靜默中互相折磨。',
		'centered ── 結局：Tragedy ──',
		'end'
	],

	'Ending_Abyss': [
		'show scene sealed_school_gate with fadeIn',
		'show character yoshiki normal at left with fadeIn',
		'show character hanako normal at right with fadeIn',
		'花子冷笑著咬破手指，將血抹在符咒上，利用佳樹最後的力量與自己的怨恨發生共鳴。那一晚，校門口傳來了慘叫聲，那些曾經霸凌過她的人被無形的黑暗拖入深淵，精神徹底崩潰。',
		'show character daiki normal at center with fadeIn',
		'大樹雖然得知真相並舉報了當年的惡行，但花子已經回不去了。她的靈魂徹底黑化，取代佳樹成為了下一個「圖書館的幽靈」。',
		'她守護著那些受欺負的人，卻也用更殘酷的方式殺死那些施暴者。大樹與花子建立了如親人般的聯繫，但他看著花子那雙空洞的雙眼，知道裡面已經沒有了溫度。',
		'正義雖然得到了伸張，但卻是以另一個惡魔的誕生為代價。圖書館依舊安靜，只是每到深夜，總能聽到紙張翻動的聲音，以及一個女孩冰冷的低語。',
		'centered ── 結局：Abyss ──',
		'end'
	]

});