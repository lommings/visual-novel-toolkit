'use strict';
/* global monogatari */

if (typeof monogatari !== 'undefined' && monogatari) {

monogatari.assets('scenes', {
  "secluded_alleyway": "secluded_alleyway/background.png",
  "aiba_apartment_interior": "aiba_apartment_interior/background.png",
  "organization_interrogation_room": "organization_interrogation_room/background.png",
  "cold_prison_cell": "cold_prison_cell/background.png",
  "busy_commercial_district": "busy_commercial_district/background.png",
  "secret_medical_lab": "secret_medical_lab/background.png",
  "private_hospital_ward": "private_hospital_ward/background.png",
  "rainy_street_lamp": "rainy_street_lamp/background.png",
  "final_dark_alley": "final_dark_alley/background.png"
});

monogatari.characters({
  "kazuya": {
    "name": "和也",
    "color": "#8b5cf6",
    "directory": "kazuya",
    "sprites": {
      "normal": "normal.png",
      "happy": "happy.png",
      "sad": "sad.png",
      "angry": "angry.png",
      "surprised": "surprised.png"
    }
  },
  "aiba": {
    "name": "相葉",
    "color": "#22c55e",
    "directory": "aiba",
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
		'show scene secluded_alleyway with fadeIn',
		'show character kazuya normal at center with fadeIn',
		'在黑暗的城市底下，有一個名為「幽影」的秘密組織，專門訓練殺手執行高難度的暗殺任務。和也，這個組織中的頂尖殺手，從小就被訓練成為冷酷無情的死神。',
		'為了確保他的忠誠與效率，組織在他體內植入了一種奇特的毒素——所有與他親密接觸的人都會在短時間內死亡。這種毒素被稱為「幽靈鏈」，不僅慢性侵蝕和也的神經系統，造成持續的疼痛，更會透過親密接觸轉移到他人體內，對普通人來說幾乎是立即致命的。',
		'和也的孤立不僅是物理上的，更是心理上的，他對這種痛苦的存在感到絕望，渴望自由。一天夜晚，完成了一次特別困難的任務後，和也因解藥效力減退，在一個僻靜的小巷中倒下了。',
		'show character kazuya normal at left',
		'show character aiba normal at right with fadeIn',
		'正巧，醫學生相葉從圖書館回家，看到倒地的和也，毫不猶豫地跑過去檢查他的狀況，焦急地詢問：「喂，你還好嗎？」',
		{
    "Choice": {
        "繼續": {
            "Text": "繼續",
            "Do": "jump AibaHelp"
        }
    }
}
	],

	'AibaHelp': [
		'show scene secluded_alleyway with fadeIn',
		'show character kazuya normal at left with fadeIn',
		'show character aiba normal at right with fadeIn',
		'相葉見和也狀況糟糕，決定不打急救電話，而是將他扶到附近24小時藥房購買止痛藥，進行簡單急救。和也稍微恢復意識，但深知這只是暫時的，他需要組織的專用解藥。',
		'相葉問他是否需要去醫院或聯繫家人，和也勉強搖頭，深知不能讓外人涉入組織事務。相葉決定帶和也回自己的公寓，這是一個簡單卻溫馨的地方。',
		'一路上，和也擔心自己傷上的毒素會感染到相葉，非常小心避免肌膚接觸。到家後，相葉扶和也躺到沙發上，為他蓋上毯子，然後去廚房熱水泡茶，準備藥物。',
		'和也感受到了相葉的善意和關懷，但內心不安，低聲提醒相葉：「你不知道我是誰，也不知道我來自哪裡。你這樣幫助我，可能會有危險。',
		'」相葉卻笑了笑，回答：「不管你是誰，現在你需要幫助，這就足夠了。我相信，每個人都值得被幫助。',
		'」',
		{
    "Choice": {
        "繼續": {
            "Text": "繼續",
            "Do": "jump FirstDilemma"
        }
    }
}
	],

	'FirstDilemma': [
		'show scene aiba_apartment_interior with fadeIn',
		'show character kazuya normal at center with fadeIn',
		'和也的眼神顯露出深深的感激和一絲困惑。他不習慣這種無條件的關懷。',
		'show character kazuya normal at left',
		'show character aiba normal at right with fadeIn',
		'相葉的出現讓和也的生活產生微妙變化，他的善良與純真讓和也開始夢想擺脫組織控制、過上自由生活。然而，現實殘酷，和也意識到自己的毒素「幽靈鏈」是對相葉的巨大風險。',
		'在公寓中，他盡力與相葉保持距離，甚至在交談時也異常疏遠。相葉曾輕聲對他說：「和也，如果你不想說也沒關係，但我希望你知道，這裡是安全的。',
		'你可以信任我。」和也心中感激，但內心掙扎與痛苦達到了頂點。',
		'他知道越是親近相葉，就越可能將他置於死地。這種壓力讓他夜難成眠，深怕無意間傷害這位無辜的善人。',
		'終於，一天清晨，城市還未完全甦醒，和也做出了艱難的決定。',
		{
    "Choice": {
        "留下簡短便條，悄無聲息地離開（原路線）": {
            "Text": "留下簡短便條，悄無聲息地離開（原路線）",
            "Do": "jump LeaveNote"
        },
        "鼓起勇氣，坦白自己的殺手身份和毒素的真相": {
            "Text": "鼓起勇氣，坦白自己的殺手身份和毒素的真相",
            "Do": "jump ConfessTruth"
        },
        "留下詳細的告別信，暗示組織的存在和其帶來的危險": {
            "Text": "留下詳細的告別信，暗示組織的存在和其帶來的危險",
            "Do": "jump DetailedFarewell"
        }
    }
}
	],

	'LeaveNote': [
		'show scene aiba_apartment_interior with fadeIn',
		'show character kazuya normal at left with fadeIn',
		'show character aiba normal at right with fadeIn',
		'和也寫下了一張簡短的便條，放在餐桌上，只寫了幾個字：「對不起，謝謝你的一切。」然後，他悄無聲息地離開了相葉的公寓，消失在晨曦的霧中。',
		'相葉醒來時發現和也不見了，桌上的便條像是一塊沉重的石頭壓在他的心頭。他感到震驚和不解，不明白為什麼和也會突然離開，不留下更多的解釋。',
		'這讓他非常擔心和也的安全，同時也對和也的過去和他所承受的痛苦感到更深的好奇和同情。回到組織之後，和也立即受到了嚴厲的審問。',
		'組織的領導者們對他的突然失踪感到懷疑和不滿，擔心他可能已經背叛或暴露了組織的秘密。他被帶到了審訊室，那是一個冷冽且昏暗的地方，牆壁上掛滿了各種審訊工具。',
		{
    "Choice": {
        "繼續": {
            "Text": "繼續",
            "Do": "jump BackToOrg"
        }
    }
}
	],

	'BackToOrg': [
		'show scene organization_interrogation_room with fadeIn',
		'show character kazuya normal at center with fadeIn',
		'「你去了哪裡？」組織的一名高級幹部瞪著和也，聲音冰冷而無情。',
		'和也低聲回應：「我受了重傷，一時趕不回來。」幹部對和也的說辭嗤之以鼻，命令手下開始對和也施加肉體上的壓力。',
		'拷打開始了，冷鐵般的鞭子和電棍成為了他們審訊的工具。每一次的打擊都讓和也痛苦難耐，皮肉撕裂的聲音在昏暗的房間裡迴響。',
		'show character kazuya normal at left',
		'show character aiba normal at right with fadeIn',
		'在瀕臨昏迷的時候，眼前浮現與相葉相處時的點點滴滴。雖然那是短暫的平靜，但回想那些慈悲與溫柔的瞬間，仿佛能聽見相葉的聲音：「不管你是誰，現在你需要幫助，這就足夠了。',
		'」這些話讓和也的內心湧起一股暖流，成為他忍受痛苦的力量。他知道，無論結局如何，他都不會讓組織的人知道相葉的存在。',
		{
    "Choice": {
        "繼續": {
            "Text": "繼續",
            "Do": "jump SecretlyWatch"
        }
    }
}
	],

	'SecretlyWatch': [
		'show scene cold_prison_cell with fadeIn',
		'show character kazuya normal at left with fadeIn',
		'show character aiba normal at right with fadeIn',
		'拷打結束後，和也被拖回自己的牢房。身體上的傷痕痛楚難忍，他蜷縮在牢房的角落，閉上眼睛，試圖在記憶中尋找那份來自相葉的溫暖和光輝。',
		'和也深知組織對他的懷疑日益增加，他的處境岌岌可危，組織很快會將自己當作棄子使用。他苦笑著想到，自己殺了那麼多人，現在卻如此畏懼死亡。',
		'這是因為在這個世界上，他有了有所留戀之人。之後每次執行任務，和也都會尋找機會，偷偷去看相葉一眼。',
		'這成了他唯一的慰藉，只要遠遠地觀望著相葉的身影，他就能感受到一絲難以言喻的幸福。他深知自己若再靠近，只會給相葉帶來無法挽回的毀滅。',
		{
    "Choice": {
        "繼續": {
            "Text": "繼續",
            "Do": "jump ChanceEncounter"
        }
    }
}
	],

	'ChanceEncounter': [
		'show scene busy_commercial_district with fadeIn',
		'show character kazuya normal at left with fadeIn',
		'show character aiba normal at right with fadeIn',
		'在一次刺殺任務中，和也偽裝成路人，在商業區的人群中潛伏。正當他調整位置，準備接近目標時，目光不經意間掃過街角的咖啡店，驚訝地發現相葉坐在那裡。',
		'和也的心猛地一震，腳步不自覺地放慢，眼睛無法從相葉的身上移開。就在這時，相葉抬頭望向街道，目光碰巧與和也相遇。',
		'相葉眼中閃過一絲驚訝，隨即換成了熱情的笑容。他站起身來，朝和也走來，聲音充滿了友善：「嘿，不是和也嗎？',
		'真巧，來這裡坐會兒吧！」和也心中一驚，本能地想逃避，但相葉的關心讓他無法動彈。',
		'他停下腳步，努力壓抑著內心的動搖，擠出一絲微笑：「相葉，沒想到會在這裡遇到你。」',
		{
    "Choice": {
        "繼續": {
            "Text": "繼續",
            "Do": "jump AvoidAiba"
        }
    }
}
	],

	'AvoidAiba': [
		'show scene busy_commercial_district with fadeIn',
		'show character kazuya normal at left with fadeIn',
		'show character aiba normal at right with fadeIn',
		'他們在街角簡短地交談，相葉的關切和真誠讓和也感到一絲前所未有的溫暖，這是他近期最真實的幸福時刻。但隨著對話深入，和也越發意識到他必須保護相葉，不能讓他捲入自己的黑暗世界。',
		'和也看了看四周，確認沒有組織的人跟蹤，他深吸一口氣，終於下定決心：「相葉，今天很高興見到你，但我得走了。請你忘記我，這對你更好。',
		'」話音剛落，和也迅速轉身，消失在人潮中。相葉站在原地，困惑而憂心，他不明白和也為何如此突然地離開，也不懂為何和也要他忘記自己。',
		'一個殺手是不能有心的，有心的殺手很快會被組織處理掉。但是，胸口的這份悸動，讓和也有活著的感覺。',
		{
    "Choice": {
        "繼續": {
            "Text": "繼續",
            "Do": "jump WorseningCondition"
        }
    }
}
	],

	'WorseningCondition': [
		'show scene cold_prison_cell with fadeIn',
		'show character kazuya normal at center with fadeIn',
		'和也的身體狀況日益惡化，組織提供的解藥對他的效用逐漸消失。原本的解藥只是暫時壓制毒素，並非真正的解毒劑，隨著時間推移，這種解藥對他的作用已經微乎其微。',
		'show character kazuya normal at left',
		'show character aiba normal at right with fadeIn',
		'這讓和也深感絕望，意識到組織已經將他視為無用之人，新的任務不過是組織設下的陷阱，旨在解決他這個棄子。面對這樣的絕境，和也做出了一個決定：他不會走向組織設下的陷阱，而是要去見相葉最後一面。',
		'在那個決定的一刻，他的心中充滿了對相葉的思念和對生命的執著。他拖著疲憊的身軀，來到相葉所在的城市。',
		'相葉是一名醫學院的學生，他的家族擁有一家專門生產和研發藥物的藥廠。這為他後續的研究提供了條件。',
		{
    "Choice": {
        "繼續": {
            "Text": "繼續",
            "Do": "jump AibaResearchDiscovery"
        }
    }
}
	],

	'AibaResearchDiscovery': [
		'show scene private_hospital_ward with fadeIn',
		'show character kazuya normal at left with fadeIn',
		'show character aiba normal at right with fadeIn',
		'在和也拖著疲憊身軀來到相葉所在的城市後，他的身體狀況已經瀕臨崩潰。相葉偶然得知和也再次出現，且狀況極差，便利用自己的醫學知識和家族藥廠的秘密療養區，悄悄將和也安置入院。',
		'他堅信只有這裡才能保證和也的安全，並爭取更多時間尋找解藥。和也的身體依然在毒素的侵蝕下飽受折磨，夜晚的痛苦與日俱增。',
		'相葉為了找到解藥而不斷努力，每次進入病房，看到和也蒼白而憔悴的臉，他的心便更加沉重，對成功的渴望也更加迫切。某個深夜，和也走進了相葉用作研究的房間。',
		'他原本只是想尋找一些止痛藥，卻在桌上發現了一些熟悉的文件和化學結構的草稿。他的目光掃過那些標記著「幽靈鏈」的資料，心中猛然一緊。',
		'他顫抖著手翻看那些檔案，裡面有詳細的毒素成分分析，甚至還有一些與組織相關的實驗報告。一個冰冷的念頭在和也的腦海中浮現。',
		{
    "Choice": {
        "冷漠地質問相葉，並將他推開（原路線）": {
            "Text": "冷漠地質問相葉，並將他推開（原路線）",
            "Do": "jump ColdQuestioning"
        },
        "忍住痛苦和疑慮，選擇相信相葉並平靜地詢問": {
            "Text": "忍住痛苦和疑慮，選擇相信相葉並平靜地詢問",
            "Do": "jump CalmInquiry"
        },
        "悄悄觀察相葉的研究，尋找更多證據": {
            "Text": "悄悄觀察相葉的研究，尋找更多證據",
            "Do": "jump SecretObservation"
        }
    }
}
	],

	'ColdQuestioning': [
		'show scene private_hospital_ward with fadeIn',
		'show character kazuya normal at left with fadeIn',
		'show character aiba normal at right with fadeIn',
		'「相葉知道得這麼多，他為什麼從來沒告訴我？」和也咬著牙，胸口像被巨石壓住一樣，「他那麼關心我的身體，是要觀察中毒者的情況嗎？',
		'我還以為……他真的喜歡我呢。」那一刻，全身刺骨的疼痛比不上心中的悲涼。',
		'第二天，相葉來到病房，準備像往常一樣幫和也檢查病情。可和也的態度卻冷得像冰。',
		'「你別再假裝了。」和也直視著相葉，眼神中充滿了悲傷和警惕。',
		'「什麼？」相葉愣住，明顯感到氣氛的異樣。',
		'「我看到了那些資料，你在研究我的毒素，對吧？」和也的聲音中有一種壓抑的痛楚，「你接近我，是不是另有目的？',
		'」相葉急忙解釋：「和也，那些研究是為了幫助你，我想找到解藥，我從沒想傷害你！」和也冷笑一聲，卻掩蓋不住眼中的失落：「是嗎？',
		'那你是不是覺得我應該感激你，把我的痛苦當作你的研究素材？」',
		{
    "Choice": {
        "繼續": {
            "Text": "繼續",
            "Do": "jump BitterDeparture"
        }
    }
}
	],

	'BitterDeparture': [
		'show scene private_hospital_ward with fadeIn',
		'show character kazuya normal at left with fadeIn',
		'show character aiba normal at right with fadeIn',
		'「和也，你對我來說不是什麼實驗體！你是……」相葉的臉色變得蒼白，他試圖伸手觸碰和也的肩膀。',
		'「你離我遠一點。」和也突然大喊，像是爆發出所有壓抑已久的情緒。',
		'相葉愣住，他的手僵在半空：「我會很小心不接觸你的肌膚，這樣不行嗎？」和也低聲說道，語氣中透著決絕，卻帶著一絲最後的溫柔：「是的。',
		'我不想讓你更靠近我。」相葉站在原地，胸口一陣酸痛，他無法接受這種距離感，卻不敢逼問，只能默默地看著和也轉身離開。',
		'夜晚的病房中，和也躺在床上，睜著眼看著天花板。他的心被矛盾和痛苦撕扯著，每當閉上眼睛，相葉的臉就會浮現在他的腦海中。',
		'在夢中，他無數次地伸出手，想要觸碰相葉的身影，但每次都在指尖即將碰到時化為虛無。「這樣也好。',
		'」和也在黑暗中輕聲自語，「只要我離開，他就不會受傷。」他的眼角滑下一滴淚。',
		{
    "Choice": {
        "繼續": {
            "Text": "繼續",
            "Do": "jump FinalDecisionPoint3"
        }
    }
}
	],

	'FinalDecisionPoint3': [
		'show scene final_dark_alley with fadeIn',
		'show character kazuya normal at center with fadeIn',
		'和也知道自己的時間不多了。組織的目光已經牢牢鎖定他，他能感受到那些無形的枷鎖正一點點收緊。',
		'show character kazuya normal at left',
		'show character aiba normal at right with fadeIn',
		'他已是組織的棄子，命不久矣。他對相葉的愛和保護欲達到頂點，此時此刻，他面臨最後的抉擇：是去見心愛之人，還是以其他方式了結自己，以確保相葉的絕對安全。',
		'他回憶起與相葉相處的短暫時光，那些溫暖的瞬間如今都成了最奢侈的念想。他的身體已經非常虛弱，毒素的侵蝕讓他的感官變得遲鈍，但他內心的掙扎卻比以往任何時候都更加劇烈。',
		'他必須在最後的時刻做出決定，一個將徹底改變他和相葉命運的決定。他深吸一口氣，心中湧起一股複雜的情緒，既有對生命的留戀，也有對相葉未來的期望。',
		'這將是他最後的任務，也是他對相葉最深沉的愛意。',
		{
    "Choice": {
        "前往相葉所在城市，見最後一面（原路線）": {
            "Text": "前往相葉所在城市，見最後一面（原路線）",
            "Do": "jump GoToAibaCity"
        },
        "利用自己僅存的力量，反抗組織，試圖逃脫並隱藏起來": {
            "Text": "利用自己僅存的力量，反抗組織，試圖逃脫並隱藏起來",
            "Do": "jump FightOrgEscape"
        },
        "直接返回組織的陷阱，犧牲自己以換取相葉的徹底安全": {
            "Text": "直接返回組織的陷阱，犧牲自己以換取相葉的徹底安全",
            "Do": "jump ReturnToTrap"
        }
    }
}
	],

	'GoToAibaCity': [
		'show scene rainy_street_lamp with fadeIn',
		'show character kazuya normal at left with fadeIn',
		'show character aiba normal at right with fadeIn',
		'和也拖著疲憊的身軀，來到相葉所在的城市。天空下著小雨，街燈昏黃，和也的步伐沉重，每走一步都像是踩在心頭上。',
		'他來到相葉的公寓樓下，遠遠地看著熟悉的窗戶。在和也遠遠觀望著相葉公寓的窗戶時，相葉剛好下樓準備到外面走走以放鬆心情。',
		'自從和也離開後，他經常感到一種不明的焦慮，仿佛心中的某部分失去了支撐。他習慣在雨中散步，感受雨滴帶來的冷靜感覺。',
		'和也站在街燈下的陰影中，雨水慢慢沁透了他的衣服，但他幾乎感覺不到寒冷。他的目光牢牢鎖定在那扇發光的窗戶上，心中充滿了既想靠近又害怕靠近的矛盾情緒。',
		{
    "Choice": {
        "繼續": {
            "Text": "繼續",
            "Do": "jump RainEncounter"
        }
    }
}
	],

	'RainEncounter': [
		'show scene rainy_street_lamp with fadeIn',
		'show character aiba normal at center with fadeIn',
		'此時，相葉戴著帽子，傘下只露出半張臉，他低頭踏步在雨中。當他走到街燈下，突然注意到一個身影站在光與影的交界處。',
		'show character aiba normal at left',
		'show character kazuya normal at right with fadeIn',
		'起初他只是覺得好奇，但當他抬頭仔細一看，即便只有微弱的光線，他也立刻認出了和也。「和也？',
		'」相葉的聲音在雨聲中顯得有些不確定，但卻帶著深深的關懷與驚喜。和也轉過身，他沒有想到會在這樣的情況下被相葉發現。',
		'他的臉上掛著疲憊而複雜的表情，深深吸了一口冷空氣，緩緩地說：「相葉……我只是想遠遠看你一眼。」相葉沒有遲疑，迅速走到和也的身邊，將他的傘伸過來與和也共撐。',
		'「為什麼要遠遠地看？如果你願意，我希望你能再來到我的身邊。',
		'」相葉的聲音堅定而溫柔。和也望著相葉，眼中閃過一絲猶豫和掙扎，但最終在相葉的堅持和那雙充滿擔憂的眼神下，他的心牆慢慢崩解。',
		'「我……我不想再逃避了。」兩人就這樣在雨中，共撐一把傘，慢慢地走回相葉的公寓。',
		{
    "Choice": {
        "繼續": {
            "Text": "繼續",
            "Do": "jump ApartmentConfession"
        }
    }
}
	],

	'ApartmentConfession': [
		'show scene aiba_apartment_interior with fadeIn',
		'show character kazuya normal at left with fadeIn',
		'show character aiba normal at right with fadeIn',
		'在相葉的公寓中，和也一直在努力保持距離，生怕自己身上的毒素會傷害到相葉。即便如此，他的眼神中充滿了對相葉的依戀與渴望。',
		'相葉試圖給予幫助和安慰，但和也始終拒絕，每次相葉靠近，和也都會畏縮甚至是驚慌地閃避。一晚，和也的痛苦變得無法忍受，他在地上打滾，每一次痙攣都讓他的呼吸更加困難。',
		'相葉聽到聲音趕來，見到這一幕，急忙上前想要幫助。「滾開！',
		'不要碰我！」和也在痛苦中大叫，聲音中帶著絕望。',
		'相葉的心感到一陣刺痛，他無法理解和也為何如此對待自己，但更多的是無法忍受看到和也這樣痛苦。「你怎麼可以這樣對待自己！',
		'我要帶你去醫院，不管你說什麼！」當相葉再次試圖接近時，和也用武技巧妙地將相葉推飛出去。',
		'「如果你看不慣我這樣，我不會再出現在你面前。」和也勉強站起身來，朝著門口蹣跚而去，深知他不能再利用相葉的善意。',
		'「我不是這個意思！」相葉有些慌張地叫道，他爬起來跟上前去，衝動地告白，「我是因為喜歡你，所以看到你這麼痛苦，我很難過想幫助你。',
		'」',
		{
    "Choice": {
        "繼續": {
            "Text": "繼續",
            "Do": "jump PoisonContactScene"
        }
    }
}
	],

	'PoisonContactScene': [
		'show scene aiba_apartment_interior with fadeIn',
		'show character kazuya normal at left with fadeIn',
		'show character aiba normal at right with fadeIn',
		'和也聽到這話後，感到一陣心酸和無力，他的身體慢慢倒下，淚水在眼眶中打轉。相葉的表白讓他的心牆最終崩塌。',
		'相葉小心地靠近倒地的和也，試圖扶他起來。和也虛弱地抬手，呼籲相葉不要接觸，「求求你不要碰我。',
		'」「你不要害怕，我不會對你做不好的事情。」相葉柔聲回答。',
		'「我不是害怕你對我做什麼不好的事，我是害怕自己會害了你。」和也說。',
		'「甚麼意思?」和也向相葉坦白了自己的身份和過去的一切，包括組織的真相和自己的掙扎。相葉聽著，雖然驚訝和害怕，但更多的是對和也的同情和理解。',
		'「抱歉給你添了那麼多麻煩，我只是...最後想來看看你。」相葉聽後震驚不已，但他的眼神更加堅定：「無論你的過去是什麼，我都不會離開你。',
		'」和也看著相葉那認真而堅定的眼神，感受到了一種前所未有的安全感。此時，相葉的手不經意間觸碰到了和也裸露的肌膚。',
		'一股無形而致命的毒素透過接觸滲進相葉體內，讓他霎時痛不欲生。',
		{
    "Choice": {
        "繼續": {
            "Text": "繼續",
            "Do": "jump SacrificeForLove"
        }
    }
}
	],

	'SacrificeForLove': [
		'show scene final_dark_alley with fadeIn',
		'show character kazuya normal at left with fadeIn',
		'show character aiba normal at right with fadeIn',
		'相葉的呼吸變得急促，劇烈的疼痛在他體內翻湧，他幾乎無法站立。和也見狀，心如刀絞，立刻取出僅有的解藥小瓶，這是他們能夠依賴的最後希望。',
		'「相葉，快喝這個！」和也在傾盆大雨中大喊，將解藥塞進相葉的手裡。',
		'相葉顫抖著握住小瓶，他明白這很可能是救命的關鍵。他強忍著混亂與痛苦，抬眼望向和也，眼裡滿是捨不得與恐懼。',
		'「和也，你…」他張口想說些什麼。「沒時間了，快喝！',
		'」和也急切地打斷他，用力把解藥推向相葉的唇邊。解藥迅速滑進相葉口中，隨著它的發揮作用，相葉體內的痛楚開始緩解，呼吸也逐漸平穩。',
		'然而，他清楚地意識到，這意味著和也放棄了自己的生命。「你為什麼要這樣做？',
		'」相葉滿含淚水地問，雨點和淚水在臉頰上交織成一體，分不清彼此。「因為我愛你，相葉。',
		'我不能讓你死在這裡。」和也的聲音依然堅定，那份溫柔在狂風驟雨中顯得愈加難得。',
		'此時，組織的追兵已經逼近。和也緊緊抓住相葉的肩膀，深深地注視他的眼睛。',
		'「跑吧，相葉，你一定要活下去。」話音剛落，和也用力將相葉推向一條陰暗的小巷，自己則毅然轉身，直面蜂擁而至的追兵，試圖用自身作為誘餌來為相葉爭取逃離的時間。',
		{
    "Choice": {
        "繼續": {
            "Text": "繼續",
            "Do": "jump Ending_UnembraceableLove"
        }
    }
}
	],

	'Ending_UnembraceableLove': [
		'show scene final_dark_alley with fadeIn',
		'show character kazuya normal at center with fadeIn',
		'當所有的喧囂平息，和也感到一股前所未有的安靜。他的身體被毒素和時間侵蝕得支離破碎，痛苦彷彿成了生命中最後的常態。',
		'然而，在他閉上眼的那一刻，世界突然變得柔軟而溫暖。他夢見自己站在一片明亮的草原上，微風輕拂，陽光灑滿每一寸土地。',
		'show character kazuya normal at left',
		'show character aiba normal at right with fadeIn',
		'他看見相葉站在不遠處，臉上帶著那抹熟悉的溫柔笑容，像是一個從未遠離的依靠。相葉向他伸出手，沒有猶豫，也沒有顧忌。',
		'「和也，過來吧。」相葉的聲音清晰而溫暖，像是穿透了所有的黑暗。',
		'和也看著他，感到一陣輕盈的喜悅，那種快要被遺忘的幸福感重新在胸口湧動。他走上前，伸出手，毫不猶豫地握住了相葉的手。',
		'他發現，自己的手不再冰冷，也沒有毒素的枷鎖，一切是那麼自然，那麼美好。「相葉，我……」和也張口想說些什麼，卻被相葉拉入了一個溫暖的擁抱。',
		'「沒事了，和也，一切都過去了。」相葉的聲音輕輕響起，像是安撫，又像是承諾。',
		'和也閉上眼睛，感受著這份久違的溫暖。他沒有再推開，也不再抗拒。',
		'他只是靜靜地享受這一刻，那些曾經的掙扎和痛苦彷彿都遠去了。「這是我能做的最好的夢了吧。',
		'」和也輕聲說，嘴角泛起一抹微笑。他的聲音低而安穩，帶著釋然。',
		'夢中的草原依然明亮，微風依舊輕柔。和也感到前所未有的滿足與平靜，這是他從未奢求過的幸福。',
		'或許這只是一場短暫的夢，但在孤獨中死去的和也，這是他生命中最美好的片刻，也是他最好的夢。相葉活了下來，但心中永遠帶著對和也的思念和悲傷。',
		'centered ── 結局：Unembraceable Love ──',
		'end'
	],

	'ConfessTruth': [
		'show scene aiba_apartment_interior with fadeIn',
		'show character kazuya normal at left with fadeIn',
		'show character aiba normal at right with fadeIn',
		'在那個清晨，和也深吸一口氣，決定面對這份突如其來的關懷。他坐在相葉床邊，輕聲喚醒他。',
		'「相葉，我有話必須對你說。」和也坦白了自己的殺手身份，以及體內「幽靈鏈」毒素的真相，包括它如何透過親密接觸致命，以及組織如何利用它控制自己。',
		'相葉聽後雖然震驚，眼神中充滿了難以置信的痛苦，但他選擇了相信。「不管你經歷了什麼，和也，我都會幫助你。',
		'」相葉堅定地說道。這個坦白讓兩人的關係不再有隔閡，但同時也將相葉置於組織的追蹤與危險之中。',
		'相葉立即利用他家族藥廠的秘密資源和醫學知識，開始與和也共同尋找解藥，希望能在組織發現之前，將和也從這場夢魘中解救出來。他們意識到，時間已經不多了。',
		{
    "Choice": {
        "繼續": {
            "Text": "繼續",
            "Do": "jump EarlyCooperation"
        }
    }
}
	],

	'EarlyCooperation': [
		'show scene secret_medical_lab with fadeIn',
		'show character aiba normal at center with fadeIn',
		'相葉動用了家族藥廠的秘密資料庫，很快便發現了「幽靈鏈」的相關檔案，驚覺這種毒素竟然是由自家藥廠研發的，並且被標記為廢棄。進一步調查，揭示了家族企業與「幽影」組織之間的暗中交易，毒素被非法用作控制工具。',
		'show character aiba normal at left',
		'show character kazuya normal at right with fadeIn',
		'這個發現讓相葉心痛不已，他意識到自己不僅要保護和也，還要揭露家族企業的黑暗面。和也得知相葉的家族涉入其中，內心充滿了複雜的情緒，既有憤怒，也有對相葉處境的擔憂。',
		'然而，相葉的堅定讓他感到一股前所未有的希望。兩人決定合作，和也提供組織的內部情報，相葉則利用藥廠資源加速解藥的研發。',
		'他們的每一步都充滿了危險，但為了共同的自由和正義，他們義無反顧。組織也很快察覺到和也的異常，並開始將調查重心轉向相葉的家族藥廠。',
		{
    "Choice": {
        "繼續": {
            "Text": "繼續",
            "Do": "jump FacingDangerTogether"
        }
    }
}
	],

	'FacingDangerTogether': [
		'show scene secret_medical_lab with fadeIn',
		'show character kazuya normal at left with fadeIn',
		'show character aiba normal at right with fadeIn',
		'組織的追蹤開始加劇，他們嗅到了背叛的氣息，並將矛頭指向了相葉的家族藥廠。和也的身體狀況也因為持續的毒素侵蝕和解藥研發的壓力而日益惡化，但相葉的堅韌和對解藥的執著成了他最大的支撐。',
		'兩人夜以繼日地工作，相葉在實驗室裡廢寢忘食，和也則利用自己對組織的了解，幫助相葉避開追蹤、獲取關鍵情報。他們經歷了數次險象環生的追擊，有時必須捨棄研究成果轉移地點，有時則要面對組織派來的殺手。',
		'每一次的危機都讓他們的心靠得更近，也讓他們對彼此的信任更加堅固。最終，經過無數次的失敗和嘗試，相葉的實驗室裡傳來了振奮人心的消息——他們找到了「幽靈鏈」的突破性解藥。',
		'這種藥物不僅能中和毒素，還能修復神經系統，讓和也徹底擺脫組織的控制。',
		{
    "Choice": {
        "繼續": {
            "Text": "繼續",
            "Do": "jump SuccessfulBreakthroughA"
        }
    }
}
	],

	'SuccessfulBreakthroughA': [
		'show scene secret_medical_lab with fadeIn',
		'show character aiba normal at center with fadeIn',
		'相葉手中握著試管，激動得幾乎無法呼吸。他們成功了！',
		'show character aiba normal at left',
		'show character kazuya normal at right with fadeIn',
		'和也的生命終於有了轉機，他將不再是組織的工具，也不再被毒素束縛。兩人緊緊相擁，淚水模糊了視線，這是他們共同努力、歷經生死換來的勝利。',
		'然而，他們深知解藥的成功只是第一步，真正的挑戰才剛剛開始。組織不會輕易放過他們，更不會讓他們的罪行被揭露。',
		'和也與相葉決定，要將這份解藥作為武器，徹底揭露「幽影」組織的罪行，以及家族藥廠在背後的黑暗交易。他們準備好了面對接下來的一切，因為他們知道，這次他們不再孤單，而是肩並肩地共同戰鬥。',
		'解藥研發的成功，也讓和也體內的毒素開始得到抑制，他的身體雖然還虛弱，但已經不再承受那種蝕骨的痛苦，這讓他在心理上得到了極大的釋放。',
		{
    "Choice": {
        "繼續": {
            "Text": "繼續",
            "Do": "jump RevealOrgSecrets"
        }
    }
}
	],

	'DetailedFarewell': [
		'show scene aiba_apartment_interior with fadeIn',
		'show character kazuya normal at left with fadeIn',
		'show character aiba normal at right with fadeIn',
		'和也在餐桌上留下了一封詳細的告別信，內容中不僅充滿了對相葉的感謝和不捨，也暗示了自己身處極端危險之中，並隱晦地提到了「幽影」組織的存在及其帶來的致命威脅，希望相葉能因此遠離。他悄無聲息地離開，消失在晨曦中。',
		'相葉醒來後讀到信，心中充滿了震驚與不解。然而，信中對於危險的暗示，以及和也異常的態度，讓相葉的醫學生直覺被觸發。',
		'他開始秘密調查和也的背景，並從和也留下的隻字片語和自己的醫學知識中，將線索導向了毒理學。他的初步探究，很快就將目標鎖定在了家族藥廠內一些高度保密的藥物研究檔案上。',
		'他意識到和也的處境遠比他想像的要危險。和也雖然暫時安全地回到了組織，但內心卻充滿了對相葉的擔憂，他不知道相葉是否會理解他的警告，更不確定自己能否保護他。',
		{
    "Choice": {
        "繼續": {
            "Text": "繼續",
            "Do": "jump AibaSecretInvestigation"
        }
    }
}
	],

	'AibaSecretInvestigation': [
		'show scene secret_medical_lab with fadeIn',
		'show character aiba normal at center with fadeIn',
		'相葉憑藉信中暗示的危險和自己醫學生的敏銳直覺，開始秘密調查。他在家族藥廠的資料庫中，循著蛛絲馬跡，逐漸接觸到一些高度機密的檔案。',
		'show character aiba normal at left',
		'show character kazuya normal at right with fadeIn',
		'令他震驚的是，這些檔案顯示，和也體內的「幽靈鏈」毒素竟然是由他自家藥廠研發的廢棄項目。進一步的追查，讓他發現家族企業與「幽影」組織之間存在著不為人知的黑暗交易，毒素被非法轉移，成為組織控制殺手的工具。',
		'這個發現讓相葉的世界觀徹底崩塌，他尊敬的家族企業竟是黑暗勢力的一部分。他意識到和也的危險遠超想像，而且自己也因為觸及了核心秘密而面臨極大的風險。',
		'相葉決定，他不能讓和也獨自承受這一切。他開始更深入地挖掘，不僅為了找到和也，也為了揭露家族企業的罪行。',
		'和也此時雖然回到了組織，但組織對他的疑慮未消，不斷安排危險任務考驗他，他深知自己已是棄子。',
		{
    "Choice": {
        "繼續": {
            "Text": "繼續",
            "Do": "jump AibaFindsTruth"
        }
    }
}
	],

	'AibaFindsTruth': [
		'show scene secret_medical_lab with fadeIn',
		'show character kazuya normal at left with fadeIn',
		'show character aiba normal at right with fadeIn',
		'相葉在秘密調查中，發現了家族藥廠與「幽影」組織之間更深層次的聯繫，以及「幽靈鏈」毒素被用作控制殺手的真相。這讓他對和也的處境有了更全面的理解，也對組織的殘酷有了更深的體會。',
		'他意識到和也的告別信並非簡單的離開，而是帶著巨大的犧牲和保護。相葉決定主動出擊，他找到和也之前偷偷窺探自己的地方，將自己的發現告知了和也。',
		'和也得知相葉不僅沒有遠離危險，反而更深入地涉入了組織的秘密，內心極度掙扎。他感激相葉的信任和勇敢，但也萬分擔憂相葉的安全。',
		'然而，相葉的坦誠和堅定，讓和也看到了合作的可能。他們決定共同面對這個龐大的敵人，相葉利用家族藥廠的資源和情報，而和也則利用他在組織中的經驗，共同尋找解藥並設法揭露組織的罪行。',
		'他們的每一步都像是走在鋼索上，但彼此的信任和愛意成為他們最大的力量。',
		{
    "Choice": {
        "繼續": {
            "Text": "繼續",
            "Do": "jump ConfrontingCrisis"
        }
    }
}
	],

	'ConfrontingCrisis': [
		'show scene secret_medical_lab with fadeIn',
		'show character kazuya normal at left with fadeIn',
		'show character aiba normal at right with fadeIn',
		'兩人決定合作後，相葉將和也轉移到家族藥廠的秘密實驗室中，開始全力研發解藥。和也的身體狀況雖日益惡化，但相葉的專業知識和日以繼夜的努力，讓解藥的研發取得了突破性進展。',
		'然而，組織也察覺到了異常，他們派出了更多追兵，試圖找出和也的藏身之處並清除所有潛在的威脅。相葉和和也面臨著前所未有的危機。',
		'實驗室經常遭到襲擊，兩人必須在保護研究成果的同時，與組織的殺手周旋。和也多次利用自己的戰鬥經驗保護相葉和實驗室，而相葉則在每次危機中尋找解藥研發的靈感，他的堅定與智慧讓和也更加確定自己的選擇。',
		'在一次激烈的衝突中，相葉受了輕傷，和也心如刀絞，但他知道，現在不是放棄的時候。在生死的邊緣，他們終於合力完成了最終的解藥，不僅能夠解除和也體內的毒素，還能讓他擺脫組織的控制。',
		{
    "Choice": {
        "繼續": {
            "Text": "繼續",
            "Do": "jump FinalPushForCure"
        }
    }
}
	],

	'FinalPushForCure': [
		'show scene secret_medical_lab with fadeIn',
		'show character kazuya normal at left with fadeIn',
		'show character aiba normal at right with fadeIn',
		'在組織的追擊下，時間緊迫，相葉和和也共同努力。相葉在秘密實驗室中夜以繼日地奮鬥，和也則在外面為他爭取時間，提供情報，並處理組織的追兵。',
		'和也的身體因解藥的突破性進展而稍有緩解，讓他能以更強的姿態與組織對抗。最終，相葉成功研發出徹底的解藥，不僅治癒了和也體內的「幽靈鏈」，也讓他擺脫了組織的控制。',
		'和也感受到身體內毒素的消退，前所未有的自由感湧上心頭。然而，他們知道這還不是結束，組織絕不會善罷甘休。',
		'兩人決定將揭露組織的罪行，以及家族藥廠在其中扮演的黑暗角色，作為他們徹底擺脫陰影的最後一戰。他們不再是受害者，而是準備好為正義而戰的戰士。',
		'他們收集了所有證據，準備向世人揭露真相。',
		{
    "Choice": {
        "繼續": {
            "Text": "繼續",
            "Do": "jump RevealOrgSecrets"
        }
    }
}
	],

	'CalmInquiry': [
		'show scene private_hospital_ward with fadeIn',
		'show character kazuya normal at left with fadeIn',
		'show character aiba normal at right with fadeIn',
		'和也深吸一口氣，壓下心中的痛苦和疑慮。他知道相葉是個善良的人，他選擇相信相葉。',
		'當相葉第二天來到病房時，和也用一種平靜但略帶質問的語氣說道：「相葉，我昨天看到了你研究『幽靈鏈』的資料。你能告訴我這是怎麼回事嗎？',
		'」相葉先是一愣，隨後眼中閃過一絲緊張，但他很快恢復了鎮定。「和也，我向你隱瞞了這些，我很抱歉。',
		'」他解釋說，自己偶然發現了家族藥廠與這種毒素的聯繫，並意識到和也的身體狀況與此有關。他之所以研究，是為了尋找解藥，希望能幫助和也擺脫控制。',
		'「我發誓，我從未把你當作實驗體，和也。你對我來說，是值得我付出一切去幫助的人。',
		'」相葉語氣堅定，眼神中充滿了真誠。和也看著相葉的眼睛，心中的冰冷逐漸消融，他選擇了相信。',
		{
    "Choice": {
        "繼續": {
            "Text": "繼續",
            "Do": "jump DeepenedTrust"
        }
    }
}
	],

	'DeepenedTrust': [
		'show scene private_hospital_ward with fadeIn',
		'show character kazuya normal at left with fadeIn',
		'show character aiba normal at right with fadeIn',
		'誤會解除後，兩人的關係更加堅固。和也對相葉的信任達到前所未有的高度，他意識到相葉冒著巨大風險在幫助自己。',
		'相葉也因為和也的坦誠而感動，更加堅定要為他找到解藥。他們開始更緊密地合作，相葉利用家族藥廠的資源和知識加速解藥的研發，而和也則將自己對組織的了解和潛在的威脅情報提供給相葉，幫助他避開追蹤。',
		'相葉發現了解藥的關鍵成分，並意識到組織為了確保和也的依賴性，刻意隱瞞了這些資訊。和也的身體雖然仍然飽受毒素的折磨，但每當看到相葉為他忙碌的身影，心中便湧起一股暖流。',
		'他知道，這不是一個人的戰鬥，他們是命運共同體。組織對和也的監視也逐漸收緊，他們感覺到和也可能正在試圖擺脫控制，這讓他們研發解藥的過程更加艱險，但兩人的決心也更加堅定。',
		{
    "Choice": {
        "繼續": {
            "Text": "繼續",
            "Do": "jump SuccessfulBreakthroughB"
        }
    }
}
	],

	'SuccessfulBreakthroughB': [
		'show scene secret_medical_lab with fadeIn',
		'show character kazuya normal at left with fadeIn',
		'show character aiba normal at right with fadeIn',
		'在不斷的嘗試與挫折中，相葉在和也的信任與支持下，憑藉超凡的毅力與智慧，終於研發出徹底的解藥。和也的身體在服用解藥後，毒素逐漸被中和，曾經的疼痛和虛弱感開始消退。',
		'他感覺到一股前所未有的輕盈與力量重新回到體內，這不僅是身體上的治癒，更是心靈上的解放。然而，他們深知解藥的成功只是戰鬥的開始，組織的威脅依然存在。',
		'他們共同努力，收集了足夠的證據，準備向世人揭露「幽影」組織的罪行以及家族藥廠在背後的黑暗交易。他們知道這將是一場艱難的鬥爭，可能會面臨生命危險，但他們不再害怕，因為他們選擇了共同面對。',
		'他們不再是孤獨的影子，而是相互扶持的戰友和愛人。他們準備為自由和正義而戰，為他們的未來和所有受害者討回公道。',
		{
    "Choice": {
        "繼續": {
            "Text": "繼續",
            "Do": "jump RevealOrgSecrets"
        }
    }
}
	],

	'SecretObservation': [
		'show scene private_hospital_ward with fadeIn',
		'show character kazuya normal at left with fadeIn',
		'show character aiba normal at right with fadeIn',
		'和也壓下了心中的痛苦和疑慮，沒有質問相葉。他選擇悄悄觀察相葉的研究，想知道相葉真正的目的。',
		'夜晚，當相葉以為和也睡著後，他會徹夜待在實驗室裡。和也透過門縫，看到相葉焦慮地翻閱資料，不斷進行實驗，甚至有時會因為實驗失敗而痛苦地捶打桌面。',
		'他看到了相葉因為疲憊而蒼白的臉，因為焦慮而緊皺的眉頭，甚至有一次，相葉在嘗試一種危險的化學反應時，險些被炸傷。和也意識到，相葉並非在利用他，而是在冒著生命危險，拼盡全力為他尋找解藥。',
		'相葉眼中的真誠和那份不顧一切的執著，讓和也心中的冰冷徹底融化。他對相葉的誤解煙消雲散，取而代之的是深深的愧疚和感激。',
		{
    "Choice": {
        "繼續": {
            "Text": "繼續",
            "Do": "jump MutualSupport"
        }
    }
}
	],

	'MutualSupport': [
		'show scene private_hospital_ward with fadeIn',
		'show character kazuya normal at left with fadeIn',
		'show character aiba normal at right with fadeIn',
		'一天早上，和也主動找到了相葉，眼神中不再有猜疑，而是充滿了堅定和支持。「相葉，讓我幫你。',
		'」和也說道，並將自己對組織的了解和戰鬥經驗，毫不保留地分享給相葉。相葉驚訝於和也的轉變，但很快便從他的眼神中讀懂了一切，兩人的心更加緊密地聯繫在一起。',
		'他們共同努力，和也協助相葉在實驗室中進行危險的實驗，利用自己的敏銳度觀察細微的變化，並在實驗室外防範組織的追蹤。相葉則在和也的協助下，加速了對「幽靈鏈」毒素的解析，並成功鎖定了研發解藥的關鍵方向。',
		'組織對和也的異常也越來越警覺，他們的追蹤和威脅日益加劇，但兩人已經做好了共同面對一切的準備。和也第一次感覺到，自己不再是孤單一人，他的生命中有了可以並肩作戰的夥伴，有了為之奮鬥的目標。',
		{
    "Choice": {
        "繼續": {
            "Text": "繼續",
            "Do": "jump SuccessfulBreakthroughC"
        }
    }
}
	],

	'SuccessfulBreakthroughC': [
		'show scene secret_medical_lab with fadeIn',
		'show character kazuya normal at left with fadeIn',
		'show character aiba normal at right with fadeIn',
		'在共同努力下，相葉成功研發出徹底的解藥，不僅治癒了和也體內的「幽靈鏈」，也讓他擺脫了組織的控制。和也體內的毒素被完全清除，困擾他多年的痛苦終於畫上句號。',
		'他感受到身體恢復了活力，心靈也獲得了前所未有的自由。這次的成功，證明了他們之間堅不可摧的信任和愛。',
		'然而，他們知道組織不會善罷甘休。和也與相葉決定，要共同揭露「幽影」組織的罪行和家族藥廠的黑暗交易。',
		'他們收集了所有證據，準備向世人揭露真相。兩人意識到這將是一場艱難的戰鬥，但他們不再懼怕，因為他們彼此擁有。',
		'他們將並肩作戰，為自己和所有受害者爭取真正的自由與正義。他們的愛情在逆境中愈發堅韌，成為彼此最強大的力量。',
		{
    "Choice": {
        "繼續": {
            "Text": "繼續",
            "Do": "jump RevealOrgSecrets"
        }
    }
}
	],

	'RevealOrgSecrets': [
		'show scene busy_commercial_district with fadeIn',
		'show character kazuya normal at left with fadeIn',
		'show character aiba normal at right with fadeIn',
		'和也與相葉在成功研發出解藥、並讓和也體內的毒素徹底清除後，意識到戰鬥並未結束。他們攜手合作，利用相葉家族藥廠的內部資料，以及和也從組織獲得的情報，逐步揭露了「幽影」組織的罪行和家族藥廠在背後進行的黑暗交易。',
		'這場揭露行動引發了巨大的震動，組織不甘失敗，展開了瘋狂的反撲。兩人經歷了重重危機，不僅要面對組織殺手的追殺，還要應對來自家族內部保守派的阻撓。',
		'和也憑藉他精湛的戰鬥技巧保護相葉，相葉則利用他的智慧和資源，將證據公之於眾。最終，他們成功地將組織的主要成員和家族藥廠的涉案高層繩之以法。',
		'在經歷了漫長而艱難的鬥爭後，和也終於獲得了真正的自由，不再是那個被「幽靈鏈」束縛的殺手。他和相葉也終於能夠卸下所有的防備，過上他們夢寐以求的平靜生活。',
		{
    "Choice": {
        "繼續": {
            "Text": "繼續",
            "Do": "jump Ending_BreakChains"
        }
    }
}
	],

	'Ending_BreakChains': [
		'show scene aiba_apartment_interior with fadeIn',
		'show character kazuya normal at left with fadeIn',
		'show character aiba normal at right with fadeIn',
		'陽光灑在兩人肩上，和也與相葉緊握著手，漫步在一個寧靜的小鎮。他們成功地揭露了「幽影」組織的罪行和家族藥廠的黑暗交易，雖然過程充滿了危險與犧牲，但最終正義得以伸張。',
		'和也體內的「幽靈鏈」毒素被徹底清除，他不再受組織的控制，也不再是那個冷酷無情的殺手。他的眼神中充滿了前所未有的溫柔與平靜，這是他從未奢望過的自由。',
		'相葉也卸下了肩上的重擔，家族藥廠在經歷洗牌後走向了正軌，由清白的人接管。他們共同經歷了生死考驗，建立了堅不可摧的信任，愛情也在這份信任中日益深厚。',
		'他們選擇了遠離城市的喧囂，在一個偏遠而美麗的地方定居，過著相守一生的幸福生活。他們不再是黑暗世界中的受害者，而是破鏈重生的自由靈魂。',
		'每一個清晨，當和也醒來看到身邊的相葉，他都會感到無比的幸福與感激，因為這一切都來之不易，也因為，他終於與相葉擁有了能相守一生的未來。',
		'centered ── 結局：破鏈重生 ──',
		'end'
	],

	'FightOrgEscape': [
		'show scene final_dark_alley with fadeIn',
		'show character kazuya normal at left with fadeIn',
		'show character aiba normal at right with fadeIn',
		'和也選擇了反抗，他沒有返回組織的陷阱，而是利用自己僅存的體力和對組織內部佈防的了解，展開了一場殊死搏鬥。他知道自己命不久矣，但這最後的戰鬥，是為自己爭取一份尊嚴，也是為了確保相葉的絕對安全。',
		'他與組織的追兵在城市邊緣展開了一場激烈的巷戰，利用地形和夜色掩護，竭盡全力與他們周旋。雖然毒素讓他的身體越來越虛弱，但他憑藉著對相葉的思念和對自由的渴望，爆發出了驚人的意志力。',
		'在付出了巨大的代價後，和也重傷逃脫，消失在組織的視野中。他知道自己不能再回到相葉身邊，那樣只會將危險帶給他。',
		'他選擇了隱姓埋名，從此過著孤獨而警惕的生活。每當夜深人靜時，他會想起相葉的笑容，那份愛意成為他活下去的唯一動力。',
		'相葉則繼續在城市中生活，心中充滿了對和也的思念和不確定的希望。',
		{
    "Choice": {
        "繼續": {
            "Text": "繼續",
            "Do": "jump Ending_LostShadow"
        }
    }
}
	],

	'Ending_LostShadow': [
		'show scene final_dark_alley with fadeIn',
		'show character kazuya normal at center with fadeIn',
		'和也成功隱匿了行蹤，從此消失在人海茫茫之中。他重獲了軀體上的自由，不再受到組織的控制，但這份自由卻是孤獨的。',
		'show character kazuya normal at left',
		'show character aiba normal at right with fadeIn',
		'他換了一個身份，在一個陌生的小鎮過著警惕而安靜的生活，不再與任何人建立深入的聯繫。每一個日出日落，他都會遠望城市的方向，心中充滿對相葉的思念，但他知道，為了相葉的絕對安全，他必須永遠地隱藏自己，成為一個真正的「幽影」。',
		'相葉則始終沒有放棄尋找和也的下落。他用盡了所有辦法，打探和也的消息，但和也就像人間蒸發了一樣。',
		'相葉的生活在和也消失後，蒙上了一層揮之不去的陰影。他常常會想起和也的眼神，想起他們短暫的相處時光，心中充滿了不確定的希望和無盡的思念。',
		'兩人的愛情，成為了一個永遠的遺憾，但相葉心中始終保有著一絲微弱的希望，或許在某個遙遠的未來，他們還有重逢的可能，只是那一天何時到來，無人知曉。',
		'centered ── 結局：消失的幽影 ──',
		'end'
	],

	'ReturnToTrap': [
		'show scene final_dark_alley with fadeIn',
		'show character kazuya normal at left with fadeIn',
		'show character aiba normal at right with fadeIn',
		'和也做出了最艱難的抉擇，他沒有反抗，也沒有逃離，而是選擇悄無聲息地返回組織設下的陷阱。他知道，這是唯一能確保相葉絕對安全的方式。',
		'如果他逃脫，組織必然會傾盡全力追捕，甚至將矛頭指向任何與他有聯繫的人，而相葉將首當其衝。他不能讓那樣的事情發生。',
		'當他回到組織的秘密基地時，他沒有抵抗，平靜地接受了組織對他的「處理」。沒有審問，沒有拷打，只有冷酷的指令和無聲的執行。',
		'組織將他視為一個已經完成使命的棄子，一個需要被徹底抹除的隱患。在生命最後的時刻，和也的心中只有相葉，他希望相葉能永遠生活在陽光下，永遠不會知道他所經歷的一切，也不會被他拖入黑暗。',
		'他的消失，將是相葉生命中永遠的謎團，也是他對相葉最深沉的愛與保護。',
		{
    "Choice": {
        "繼續": {
            "Text": "繼續",
            "Do": "jump SilentProcessing"
        }
    }
}
	],

	'SilentProcessing': [
		'show scene cold_prison_cell with fadeIn',
		'show character kazuya normal at center with fadeIn',
		'和也的消失是徹底而無聲的，組織像抹去一條痕跡般，將他秘密處理。他的存在，從此在「幽影」組織的檔案中被徹底抹除，仿佛從未在這個世界上出現過。',
		'show character kazuya normal at left',
		'show character aiba normal at right with fadeIn',
		'相葉再也沒有收到和也的任何消息。一開始，他還抱著希望，尋找、等待，但隨著時間的推移，所有的線索都石沉大海。',
		'和也的失蹤對相葉來說是一個巨大的謎團，他無法理解，也無法釋懷。曾經的關懷和愛意，最終被埋葬在無盡的沉默中。',
		'相葉的生活雖然恢復了平靜，但他心中對和也的思念和困惑卻從未停止。他時常會想起和也最後的身影，以及他那雙複雜而痛苦的眼睛。',
		'和也的選擇，讓相葉免於了組織的追殺，但他卻永遠無法得知這份犧牲，這份無法言喻的愛。和也像一個真正的幽影，徹底消失，只留下相葉在陽光下，帶著永遠的遺憾與未解的謎團生活著。',
		{
    "Choice": {
        "繼續": {
            "Text": "繼續",
            "Do": "jump Ending_SilentEnd"
        }
    }
}
	],

	'Ending_SilentEnd': [
		'show scene aiba_apartment_interior with fadeIn',
		'show character kazuya normal at left with fadeIn',
		'show character aiba normal at right with fadeIn',
		'在城市的一隅，相葉獨自生活著。歲月流逝，和也的消失始終是他心中一個無法觸及的痛點。',
		'他嘗試過各種方式去尋找，去打聽，但所有關於和也的線索都像沙子一樣從指縫中溜走，不留痕跡。他從未知道和也為了保護他，選擇了默默返回組織的陷阱，被秘密處理。',
		'在相葉的記憶中，和也依然是那個在雨夜突然出現，又突然消失的神秘男子。他曾帶給他溫暖，也曾帶給他無盡的困惑。',
		'相葉偶爾會凝視窗外，希望能在人群中再次發現那個熟悉的身影，但每一次都只是失望。他的生活重歸平靜，但心底深處，總有一塊地方，被和也的存在與其未解的命運佔據著。',
		'兩人的愛意最終隨著時間被埋葬在無盡的沉默中，成為一段永遠沒有結局的故事。相葉活下來了，但他失去了一個可以愛的人，以及所有關於他的真相。',
		'他的人生，從此多了一份寂靜的思念和無法填補的空白。',
		'centered ── 結局：無聲的終結 ──',
		'end'
	]

});

} // end if monogatari