"""Original Class 1 study guides aligned to the current NCERT textbooks."""
from __future__ import annotations

from dataclasses import dataclass

LessonFields = tuple[str, str, str, str, str]


@dataclass(frozen=True)
class LessonText:
    focus: str
    learn: str
    activity: str
    check: str
    answer: str


@dataclass(frozen=True)
class StudyLesson:
    id: str
    chapter_en: str
    chapter_hi: str
    en: LessonText
    hi: LessonText


@dataclass(frozen=True)
class StudyCourse:
    id: str
    title_en: str
    title_hi: str
    book_en: str
    book_hi: str
    source_url: str
    lessons: tuple[StudyLesson, ...]
    source_url_hi: str | None = None


def _lesson(
    lesson_id: str,
    chapter_en: str,
    chapter_hi: str,
    en: LessonFields,
    hi: LessonFields,
) -> StudyLesson:
    return StudyLesson(
        lesson_id, chapter_en, chapter_hi,
        LessonText(*en), LessonText(*hi),
    )


CLASS_1_STUDY_COURSES: dict[str, StudyCourse] = {
    "math": StudyCourse(
        "math", "Mathematics", "गणित", "Joyful Mathematics", "आनंदमय गणित",
        "https://ncert.nic.in/textbook/pdf/aejm1ps.pdf",
        (
            _lesson("m01", "Finding the Furry Cat!", "रोएँदार बिल्ली को ढूँढ़ो",
                    ("Position and comparison", "Use words such as above, below, near, far, inside and outside to describe where things are. Compare groups by matching their objects.", "Place a toy beside, inside and under a box. Ask a partner to describe each position.", "A ball is under a chair. Where is the ball?", "Under the chair."),
                    ("स्थान और तुलना", "ऊपर, नीचे, पास, दूर, अंदर और बाहर जैसे शब्दों से वस्तुओं की जगह बताइए। वस्तुओं को एक-एक करके मिलाकर समूहों की तुलना कीजिए।", "खिलौने को डिब्बे के पास, अंदर और नीचे रखें। साथी से हर स्थिति बताने को कहें।", "गेंद कुर्सी के नीचे है। गेंद कहाँ है?", "कुर्सी के नीचे।")),
            _lesson("m02", "What is Long? What is Round?", "क्या लंबा है? क्या गोल है?",
                    ("Shapes and measurable length", "Notice circles, triangles, squares and rectangles around you. Compare two objects directly to decide which is longer or shorter.", "Find one round object and one object with a straight edge. Put two pencils side by side and compare their lengths.", "Which is longer: a 10-cm pencil or a 6-cm pencil?", "The 10-cm pencil."),
                    ("आकार और लंबाई", "आसपास वृत्त, त्रिभुज, वर्ग और आयत पहचानिए। दो वस्तुओं को साथ रखकर उनकी लंबाई की तुलना कीजिए।", "एक गोल और एक सीधी किनारी वाली वस्तु ढूँढ़ें। दो पेंसिल साथ रखकर लंबाई देखें।", "10 सेमी और 6 सेमी की पेंसिल में कौन लंबी है?", "10 सेमी की पेंसिल।")),
            _lesson("m03", "Mango Treat", "आम की दावत",
                    ("Counting 1 to 9", "Count objects one at a time, say number names in order and match each number name to a group of objects.", "Count up to nine safe household objects. Touch each object once as you count.", "How many objects are in a group of seven?", "Seven."),
                    ("1 से 9 तक गिनती", "वस्तुओं को एक-एक करके गिनें, संख्या-नाम क्रम से बोलें और संख्या को वस्तुओं के समूह से मिलाएँ।", "घर की नौ सुरक्षित वस्तुओं तक गिनें। गिनते समय हर वस्तु को एक बार छुएँ।", "सात वस्तुओं के समूह में कितनी वस्तुएँ हैं?", "सात।")),
            _lesson("m04", "Making 10", "10 बनाना",
                    ("Number pairs to 10", "A group of ten can be split into two smaller groups in different ways, such as 6 and 4 or 7 and 3.", "Take ten counters. Separate them into two groups, then say how many are in each group.", "Ten counters are split into 8 and ___.", "2."),
                    ("10 के संख्या-जोड़े", "दस वस्तुओं को अलग-अलग तरीकों से दो समूहों में बाँटा जा सकता है, जैसे 6 और 4 या 7 और 3।", "दस गिनने वाली वस्तुएँ लें। उन्हें दो समूहों में बाँटकर हर समूह की संख्या बोलें।", "दस वस्तुओं को 8 और ___ में बाँटा।", "2।")),
            _lesson("m05", "How Many?", "कितने?",
                    ("Single-digit addition and subtraction", "Adding joins groups. Subtracting takes some away. Use objects or drawings to show what happens.", "Draw five dots, add two, then cross out three. Count what remains after each step.", "There are 4 birds and 2 more arrive. How many birds now?", "6 birds."),
                    ("एक अंकीय जोड़ और घटाव", "जोड़ने से समूह मिलते हैं। घटाने में कुछ वस्तुएँ कम होती हैं। वस्तुओं या चित्रों से दिखाएँ।", "पाँच बिंदु बनाएँ, दो और जोड़ें, फिर तीन काट दें। हर बार बची संख्या गिनें।", "4 पक्षी हैं और 2 और आ गए। अब कितने पक्षी हैं?", "6 पक्षी।")),
            _lesson("m06", "Vegetable Farm", "सब्ज़ियों का खेत",
                    ("Addition and subtraction up to 20", "Count on to add small groups and count back to subtract. Keep track of the starting number and each step.", "Draw 12 vegetables. Add 3 more, then take away 4. Count the result aloud.", "There are 11 carrots. If 2 are picked, how many remain?", "9 carrots."),
                    ("20 तक जोड़ और घटाव", "छोटे समूह जोड़ने के लिए आगे गिनें और घटाने के लिए पीछे गिनें। शुरुआती संख्या और हर कदम याद रखें।", "12 सब्ज़ियाँ बनाएँ। 3 और जोड़ें, फिर 4 हटा दें। उत्तर ज़ोर से गिनें।", "11 गाजर में से 2 तोड़ी गईं। कितनी बचीं?", "9 गाजर।")),
            _lesson("m07", "Lina's Family", "लीना का परिवार",
                    ("Comparing and measuring", "Describe an object as longer, shorter, taller or heavier by comparing it with another object. Use the same non-standard unit each time.", "Measure a book using hand spans. Measure it again with the same hand and compare with a pencil.", "Which is longer: a book measuring 4 hand spans or one measuring 3?", "The book measuring 4 hand spans."),
                    ("तुलना और माप", "दो वस्तुओं की तुलना करके लंबा, छोटा, ऊँचा या भारी बताइए। हर बार मापने की एक ही गैर-मानक इकाई अपनाएँ।", "किताब को हाथ की एक ही चौड़ाई से मापें। फिर पेंसिल से तुलना करें।", "4 हथेली-चौड़ाई वाली किताब लंबी है या 3 वाली?", "4 हथेली-चौड़ाई वाली किताब।")),
            _lesson("m08", "Fun with Numbers", "संख्याओं के साथ मज़ा",
                    ("Numbers 21 to 99", "Two-digit numbers have tens and ones. For example, 34 is 3 tens and 4 ones.", "Bundle sticks into groups of ten. Make 26 with two bundles and six loose sticks.", "How many tens and ones are in 42?", "4 tens and 2 ones."),
                    ("21 से 99 तक संख्याएँ", "दो अंकों की संख्या में दहाइयाँ और इकाइयाँ होती हैं। उदाहरण के लिए, 34 में 3 दहाइयाँ और 4 इकाइयाँ हैं।", "तिनकों को दस-दस के समूह में बाँधें। दो बंडल और छह खुले तिनकों से 26 बनाएँ।", "42 में कितनी दहाइयाँ और कितनी इकाइयाँ हैं?", "4 दहाइयाँ और 2 इकाइयाँ।")),
            _lesson("m09", "Utsav", "उत्सव",
                    ("Repeating patterns", "A pattern repeats a group in the same order. Look for the part that repeats to decide what comes next.", "Make a pattern with leaves and stones: leaf, stone, leaf, stone. Ask a partner what comes next.", "Red, blue, red, blue, red, ___. What comes next?", "Blue."),
                    ("दोहराते हुए पैटर्न", "पैटर्न में वस्तुओं का समूह उसी क्रम में दोहराता है। अगली वस्तु जानने के लिए दोहरने वाला भाग पहचानें।", "पत्ते और कंकड़ से क्रम बनाएँ: पत्ता, कंकड़, पत्ता, कंकड़। साथी से अगली वस्तु पूछें।", "लाल, नीला, लाल, नीला, लाल, ___। अगला रंग क्या है?", "नीला।")),
            _lesson("m10", "How do I Spend my Day?", "मैं अपना दिन कैसे बिताता हूँ?",
                    ("Daily order and time", "Put familiar events in order: morning, afternoon, evening and night. Use before and after to explain a daily routine.", "Draw three things you do in a day and arrange them from first to last.", "Does breakfast usually happen before or after bedtime?", "Before bedtime."),
                    ("दिन का क्रम और समय", "परिचित कामों को सुबह, दोपहर, शाम और रात के क्रम में रखें। दिनचर्या बताने के लिए पहले और बाद में कहें।", "दिन में किए जाने वाले तीन काम बनाएँ और पहले से आखिरी तक क्रम में रखें।", "नाश्ता आम तौर पर सोने से पहले होता है या बाद में?", "सोने से पहले।")),
            _lesson("m11", "How Many Times?", "कितनी बार?",
                    ("Equal groups and early multiplication", "Repeated equal groups can be counted by adding the same amount again. Three groups of 2 make 2 + 2 + 2.", "Put two buttons in each of three cups. Count all the buttons by ones.", "How many wheels are on two bicycles?", "4 wheels."),
                    ("बराबर समूह और गुणा की शुरुआत", "बराबर समूहों को समान संख्या बार-बार जोड़कर गिन सकते हैं। 2 के तीन समूह 2 + 2 + 2 होते हैं।", "तीन कटोरियों में हर एक में दो बटन रखें। सभी बटन एक-एक करके गिनें।", "दो साइकिलों में कुल कितने पहिए हैं?", "4 पहिए।")),
            _lesson("m12", "How Much Can We Spend?", "हम कितना खर्च कर सकते हैं?",
                    ("Recognising and comparing money", "Coins and notes represent different amounts. Count a small set of coins and compare totals before choosing what can be bought.", "With pretend coins, make the same small total in two different ways.", "A toy costs 5 rupees. Do 2 rupees and 3 rupees make enough?", "Yes, 5 rupees."),
                    ("पैसों को पहचानना और तुलना", "सिक्के और नोट अलग-अलग मूल्य बताते हैं। छोटी राशि गिनें और खरीदने से पहले कुल रकम की तुलना करें।", "नकली सिक्कों से एक छोटी राशि दो अलग-अलग तरीकों से बनाएँ।", "एक खिलौना 5 रुपये का है। क्या 2 और 3 रुपये पर्याप्त हैं?", "हाँ, 5 रुपये।")),
            _lesson("m13", "So Many Toys", "इतने सारे खिलौने",
                    ("Sorting and simple data", "Sort objects using one feature such as colour or shape. Count each group and compare which has more or fewer.", "Sort four familiar objects by colour. Draw one mark for every object in each group.", "Which group has more: 3 red objects or 2 blue objects?", "The group of 3 red objects."),
                    ("वर्गीकरण और सरल जानकारी", "वस्तुओं को रंग या आकार जैसी एक विशेषता के आधार पर छाँटें। हर समूह गिनें और अधिक-कम की तुलना करें।", "चार परिचित वस्तुओं को रंग के आधार पर छाँटें। हर समूह की वस्तु के लिए एक निशान बनाएँ।", "किस समूह में अधिक हैं: 3 लाल वस्तुएँ या 2 नीली?", "3 लाल वस्तुओं वाला समूह।")),
        ),
        "https://ncert.nic.in/textbook/pdf/ahjm1ps.pdf",
    ),
    "english": StudyCourse(
        "english", "English", "अंग्रेज़ी", "Mridang", "मृदंग",
        "https://ncert.nic.in/textbook/pdf/aemr1ps.pdf",
        (
            _lesson("e01", "Two Little Hands", "दो छोटे हाथ",
                    ("Listening, speaking and body words", "Listen to a short rhyme, notice repeated words and name familiar body parts. Join in with actions.", "Say a simple action rhyme with a partner and point to the body part you name.", "Which body part helps you clap?", "Hands."),
                    ("सुनना, बोलना और शरीर के शब्द", "छोटी कविता सुनें, दोहराए गए शब्द पहचानें और शरीर के अंगों के नाम बोलें। क्रियाओं के साथ जुड़ें।", "साथी के साथ क्रिया वाली छोटी कविता बोलें और बताए गए अंग की ओर इशारा करें।", "ताली बजाने में कौन-सा अंग मदद करता है?", "हाथ।")),
            _lesson("e02", "Greetings", "अभिवादन",
                    ("Polite greetings and introductions", "Use a greeting, say your name and listen while another person introduces themselves.", "Take turns greeting a partner and saying, “My name is …”.", "What can you say when you meet someone in the morning?", "Good morning."),
                    ("विनम्र अभिवादन और परिचय", "अभिवादन करें, अपना नाम बताएँ और दूसरे व्यक्ति का परिचय ध्यान से सुनें।", "बारी-बारी से साथी का अभिवादन करें और कहें, “My name is …”.", "सुबह किसी से मिलने पर क्या कह सकते हैं?", "Good morning.")),
            _lesson("e03", "Picture Time", "चित्रों का समय",
                    ("Picture reading and describing", "Look carefully at a picture. Name people, animals or objects and say one thing each is doing.", "Choose a picture and describe three things you can see using “I see …”.", "What question can you ask about a person in a picture?", "“What is the person doing?”"),
                    ("चित्र पढ़ना और वर्णन", "चित्र को ध्यान से देखें। लोगों, जानवरों या वस्तुओं के नाम बताएँ और वे क्या कर रहे हैं कहें।", "एक चित्र चुनें और “I see …” से दिखने वाली तीन चीज़ें बताएँ।", "चित्र में किसी व्यक्ति के बारे में कौन-सा प्रश्न पूछ सकते हैं?", "“What is the person doing?”")),
            _lesson("e04", "The Cap-seller and the Monkeys", "टोपीवाला और बंदर",
                    ("Story order and actions", "A story has events in an order. Listen for what happens first, next and at the end.", "Draw three boxes for the beginning, middle and end of a familiar story.", "Which comes first: the beginning or the end?", "The beginning."),
                    ("कहानी का क्रम और क्रियाएँ", "कहानी की घटनाएँ एक क्रम में होती हैं। सुनें कि पहले, फिर और अंत में क्या हुआ।", "परिचित कहानी की शुरुआत, बीच और अंत के लिए तीन खाने बनाएँ।", "पहले क्या आता है: शुरुआत या अंत?", "शुरुआत।")),
            _lesson("e05", "A Farm", "एक खेत",
                    ("Farm animals and simple sentences", "Name familiar farm animals and describe them with a short sentence, such as “A cow gives milk.”", "Name an animal, tell one thing it does and draw it.", "Which animal lays eggs: a hen or a cow?", "A hen."),
                    ("खेत के जानवर और सरल वाक्य", "खेत के परिचित जानवरों के नाम बताएँ और छोटा वाक्य बोलें, जैसे “A cow gives milk.”", "एक जानवर का नाम लें, उसका एक काम बताएँ और उसका चित्र बनाएँ।", "अंडे कौन देता है: मुर्गी या गाय?", "मुर्गी।")),
            _lesson("e06", "Fun with Pictures", "चित्रों के साथ मज़ा",
                    ("Vocabulary and visual clues", "Pictures give clues about meaning. Match a spoken word to the object or action it names.", "Look at a picture scene and make a list of five English words for things you recognise.", "If a picture shows a ball, which word names it?", "Ball."),
                    ("शब्दावली और चित्र-संकेत", "चित्र अर्थ समझने के संकेत देते हैं। बोले गए शब्द को उससे जुड़ी वस्तु या क्रिया से मिलाएँ।", "चित्र देखकर पहचानी गई पाँच चीज़ों के अंग्रेज़ी नाम बोलें।", "चित्र में गेंद हो तो उसे कौन-सा शब्द बताता है?", "Ball.")),
            _lesson("e07", "The Food We Eat", "हम जो भोजन खाते हैं",
                    ("Food words and preferences", "Name everyday foods and use a complete phrase to say what you like or eat.", "Ask a family member, “What food do you like?” and report the answer.", "Complete: “I like to eat ___.”", "Any suitable food word."),
                    ("भोजन के शब्द और पसंद", "रोज़मर्रा के भोजन के नाम बताएँ और अपनी पसंद या भोजन के बारे में पूरा वाक्य बोलें।", "परिवार के किसी सदस्य से पूछें, “What food do you like?” और उनका उत्तर बताएँ।", "पूरा करें: “I like to eat ___.”", "कोई भी उपयुक्त भोजन का शब्द।")),
            _lesson("e08", "The Four Seasons", "चार ऋतुएँ",
                    ("Weather and describing words", "Notice that weather changes. Use describing words such as hot, cold, rainy and sunny.", "Draw what you wear on a sunny day and on a rainy day. Name each item in English.", "Which word describes a day with much rain?", "Rainy."),
                    ("मौसम और वर्णन के शब्द", "ध्यान दें कि मौसम बदलता है। hot, cold, rainy और sunny जैसे वर्णन के शब्द बोलें।", "धूप और बारिश वाले दिन के कपड़े बनाएँ। हर वस्तु का अंग्रेज़ी नाम लें।", "जिस दिन बहुत बारिश हो, उसके लिए कौन-सा शब्द है?", "Rainy.")),
            _lesson("e09", "Anandi's Rainbow", "आनंदी का इंद्रधनुष",
                    ("Colours and observation", "Name familiar colours and notice that a rainbow shows several colours together.", "Find three coloured objects and say, “The ___ is ___.”", "What colour do you see on a green leaf?", "Green."),
                    ("रंग और अवलोकन", "परिचित रंगों के नाम बताएँ और देखें कि इंद्रधनुष में कई रंग साथ दिखाई देते हैं।", "तीन रंगीन वस्तुएँ ढूँढ़कर कहें, “The ___ is ___.”", "हरे पत्ते में कौन-सा रंग दिखाई देता है?", "Green.")),
        ),
    ),
    "hindi": StudyCourse(
        "hindi", "Hindi", "हिंदी", "Sarangi", "सारंगी",
        "https://ncert.nic.in/textbook/pdf/ahsr1ps.pdf",
        (
            _lesson("h01", "Meena's Family", "मीना का परिवार",
                    ("Family words and listening", "Listen to and say family words. Practise speaking in complete turns during a short conversation.", "Draw your family and say one sentence about a family member.", "Name one person in a family.", "Any suitable answer."),
                    ("परिवार के शब्द और सुनना", "परिवार के लोगों के नाम सुनें और बोलें। छोटी बातचीत में अपनी बात पूरी करके कहने का अभ्यास करें।", "अपने परिवार का चित्र बनाएँ और एक सदस्य के बारे में एक वाक्य बोलें।", "परिवार में रहने वाले एक व्यक्ति का नाम बताइए।", "कोई भी उपयुक्त उत्तर।")),
            _lesson("h02", "Dada-Dadi", "दादा-दादी",
                    ("Respectful conversation", "Listen carefully to elders. Ask politely about their experiences and stories.", "Ask an elder about a game they played long ago, then draw it.", "What should we do while someone tells a story?", "Listen carefully."),
                    ("आदर से बातचीत", "बड़ों की बातें ध्यान से सुनें। उनसे जुड़े अनुभवों और कहानियों के बारे में विनम्रता से प्रश्न पूछें।", "दादा-दादी या किसी बड़े से एक पुरानी खेल-कहानी सुनें और उसका चित्र बनाएँ।", "कहानी सुनते समय हमें क्या करना चाहिए?", "ध्यान से सुनना।")),
            _lesson("h03", "Reena's Day", "रीना का दिन",
                    ("Daily routine and sequence", "Put daily activities in order from morning to evening. Say each activity clearly.", "Name three things you do in order: first, next and last.", "Does waking up happen at the beginning or end of the day?", "At the beginning."),
                    ("दिनचर्या और क्रम", "दिन के कामों को सुबह से शाम तक क्रम में बताइए। कामों के नाम स्पष्ट बोलें।", "अपने दिन के तीन काम क्रम से बताएँ: पहले, फिर और अंत में।", "सुबह उठना दिन की शुरुआत में होता है या अंत में?", "शुरुआत में।")),
            _lesson("h04", "Rani Too", "रानी भी",
                    ("Belonging and taking turns", "Notice what story characters do and feel. Wait for your turn when playing together.", "Make a short conversation with two toys and let each toy have a turn to speak.", "What should you do when a friend is speaking?", "Listen to them."),
                    ("अपनापन और बारी लेना", "कहानी सुनते समय पात्रों के काम और भाव पहचानें। मिल-जुलकर खेलने में अपनी बारी की प्रतीक्षा करें।", "दो खिलौनों से छोटी बातचीत बनाएँ और हर पात्र को बोलने की बारी दें।", "खेल में साथी बोल रहा हो तो हमें क्या करना चाहिए?", "उसकी बात सुननी चाहिए।")),
            _lesson("h05", "Sweets", "मिठाई",
                    ("Food words and describing", "Learn words for foods, tastes and colours. Respect your own and other people's preferences.", "Draw a favourite sweet and say its name and colour.", "Name one sweet.", "Any suitable answer."),
                    ("भोजन के शब्द और वर्णन", "भोजन के नाम, स्वाद और रंग बताने वाले शब्द सीखें। अपनी पसंद और दूसरों की पसंद का आदर करें।", "एक पसंदीदा मिठाई बनाएँ और उसका नाम तथा रंग बताएँ।", "मिठाई का एक नाम बताइए।", "कोई भी उपयुक्त उत्तर।")),
            _lesson("h06", "Three Friends", "तीन साथी",
                    ("Friendship and story talk", "Identify story characters and talk about how friends help one another.", "Draw one way to help a friend and say a sentence about it.", "How does a good friend behave?", "A good friend helps and plays together."),
                    ("दोस्ती और कहानी पर बातचीत", "कहानी के पात्रों को पहचानें और बताएं कि साथी एक-दूसरे की मदद कैसे करते हैं।", "दोस्त की मदद करने का एक तरीका चित्र में दिखाएँ और उस पर एक वाक्य बोलें।", "अच्छा साथी कैसा व्यवहार करता है?", "वह मदद करता और मिलकर खेलता है।")),
            _lesson("h07", "Oh, My Horse!", "वाह, मेरे घोड़े!",
                    ("Animals and expressive words", "Say animal names and words for how they move. Enjoy a poem using voice and actions.", "Move like a horse and say one sentence about a horse.", "How can a horse move?", "It can run."),
                    ("जानवर और भावपूर्ण शब्द", "जानवरों के नाम और उनकी चाल बताने वाले शब्द बोलें। आवाज़ और हाव-भाव से कविता का आनंद लें।", "घोड़े की चाल की नकल करें और घोड़े के बारे में एक वाक्य बोलें।", "घोड़ा किस तरह चलता है?", "वह दौड़ सकता है।")),
            _lesson("h08", "The Snake in Danger", "खतरे में साँप",
                    ("Animals and safety", "Do not disturb animals. Keep away from an unfamiliar animal and tell an adult.", "Act out two safe things to do if you see an unfamiliar animal.", "What should you do if you see an unfamiliar snake?", "Stay away and tell an adult."),
                    ("जानवर और सुरक्षा", "जानवरों को परेशान न करें। अनजान जानवर से दूरी रखें और किसी बड़े को बताएं।", "किसी अनजान जानवर को देखकर सुरक्षित रहने के दो तरीके अभिनय से दिखाएँ।", "अनजान साँप दिखे तो क्या करना चाहिए?", "दूर रहें और बड़े को बताएँ।")),
            _lesson("h09", "The Potato Road", "आलू की सड़क",
                    ("Imagination and describing", "Listen to descriptions of places and events in an imaginary story. Use pictures to explore new words.", "Draw a funny road made of vegetables and say who might travel on it.", "Is the story's road real or imaginary?", "Imaginary."),
                    ("कल्पना और वर्णन", "कल्पना से बनी कहानी में जगहों और घटनाओं का वर्णन सुनें। नए शब्दों के अर्थ चित्रों से समझें।", "सब्ज़ियों से बनी एक मज़ेदार सड़क बनाएँ और बताएं कि उस पर कौन चलेगा।", "कहानी की सड़क असली है या कल्पना की?", "कल्पना की।")),
            _lesson("h10", "Swinging Along", "झूलम-झूली",
                    ("Rhythm and repeated sounds", "Notice rhythm and repeated sounds in a poem. Listen and repeat words.", "Clap a short, gentle rhythm and repeat it.", "What can repeat in a poem?", "Words or sounds."),
                    ("लय और दोहरती ध्वनियाँ", "कविता में लय और बार-बार आने वाली ध्वनियाँ पहचानें। सुनकर शब्दों को दोहराएँ।", "धीरे-धीरे ताली बजाकर छोटी लय बनाएँ और उसे दोहराएँ।", "कविता सुनते समय कौन-सी चीज़ दोहर सकती है?", "शब्द या ध्वनि।")),
            _lesson("h11", "Corn", "भुट्टे",
                    ("Food and observation words", "Describe the colour, shape and feel of food. Handle food cleanly.", "Look at corn or another vegetable and say three words about it.", "Is corn food or a toy?", "Food."),
                    ("भोजन और अवलोकन के शब्द", "खाने की चीज़ों को देखकर उनका रंग, आकार और बनावट बताएं। भोजन को साफ़-सुथरे ढंग से संभालें।", "भुट्टे या किसी दूसरी सब्ज़ी को देखकर उसके बारे में तीन शब्द बोलें।", "भुट्टा भोजन है या खिलौना?", "भोजन।")),
            _lesson("h12", "Puffed Roti", "फूली रोटी",
                    ("Everyday process words", "Name and sequence steps connected with preparing food. Stay near kitchen heat only with adult supervision.", "Draw the steps for making roti in order and ask an adult about kitchen safety.", "Whose help do you need near hot things in the kitchen?", "An adult's."),
                    ("रोज़मर्रा के कामों के शब्द", "घर के भोजन से जुड़े कामों के नाम सुनें और क्रम में बताएं। रसोई के पास केवल बड़े की देखरेख में रहें।", "रोटी बनने के कामों को चित्रों में क्रम से दिखाएँ और बड़े से सुरक्षित तरीके पूछें।", "रसोई में गर्म चीज़ों के पास किसकी मदद चाहिए?", "किसी बड़े की।")),
            _lesson("h13", "The Fair", "मेला",
                    ("Places and people", "Name people and things seen at a fair or market. Tell about an experience in order.", "Draw a fair and name three things you can see there.", "Name one thing you might see at a fair.", "Any suitable answer."),
                    ("जगहें और लोग", "किसी मेले या बाज़ार में दिखने वाले लोगों और चीज़ों के नाम बताएं। अपने अनुभव को क्रम से सुनाएँ।", "मेले का चित्र बनाएँ और उसमें दिखने वाली तीन चीज़ें बताएं।", "मेले में दिखने वाली एक चीज़ का नाम बताइए।", "कोई भी उपयुक्त उत्तर।")),
            _lesson("h14", "Barkha and Megha", "बरखा और मेघा",
                    ("Rain and descriptive language", "Learn words about rain and describe the weather. Notice clouds and rainfall.", "Draw a rainy day and name things shown in your picture.", "What might you see in the sky when it rains?", "Clouds."),
                    ("बारिश और वर्णन के शब्द", "बारिश से जुड़े शब्द सुनें और मौसम का वर्णन करें। बादलों और वर्षा को ध्यान से देखें।", "बारिश के दिन का चित्र बनाएँ और उसमें दिखने वाली चीज़ों के नाम बोलें।", "बारिश में आसमान में क्या दिखाई दे सकता है?", "बादल।")),
            _lesson("h15", "Holi", "होली",
                    ("Festivals and respectful choices", "Talk about festivals and respect everyone's preferences. Celebrate safely, cleanly and with consent.", "Draw a family festival and describe one kind tradition.", "Should you ask before putting colour on someone?", "Yes."),
                    ("त्योहार और सम्मानपूर्ण व्यवहार", "त्योहारों के बारे में बात करें और सबकी पसंद का सम्मान करें। सुरक्षित, साफ़ और सहमति से मनाने की बात सीखें।", "परिवार के किसी त्योहार का चित्र बनाएँ और एक अच्छी परंपरा बताएँ।", "क्या त्योहार पर किसी पर रंग डालने से पहले पूछना चाहिए?", "हाँ।")),
            _lesson("h16", "Plant a Tree on Your Birthday", "जन्मदिवस पर पेड़ लगाओ",
                    ("Plants and caring for nature", "Plants are living things and need care. Trees give shade and help keep places green.", "Draw yourself watering or caring for a plant.", "What can we give a plant to help care for it?", "Water and care."),
                    ("पौधे और प्रकृति की देखभाल", "पौधे जीवित होते हैं और उनकी देखभाल करनी चाहिए। पेड़ हमें छाया देते हैं और आसपास को हरा-भरा बनाते हैं।", "किसी पौधे को पानी देने या उसकी देखभाल करने का चित्र बनाएँ।", "पौधे की देखभाल के लिए हम क्या दे सकते हैं?", "पानी और ध्यान।")),
            _lesson("h17", "Wind", "हवा",
                    ("Senses and natural forces", "We cannot see air moving, but can notice its effects on leaves or a kite. Clean air is important.", "Fan gently with paper and notice what the moving air changes.", "What can show that air is moving?", "Moving leaves."),
                    ("इंद्रियाँ और प्रकृति", "हवा दिखाई नहीं देती, पर पत्तों या पतंग की गति से उसका असर देख सकते हैं। हवा को साफ़ रखना ज़रूरी है।", "कागज़ का पंखा धीरे चलाएँ और महसूस करें कि हवा से क्या बदलता है।", "हवा का पता किससे चल सकता है?", "चलती पत्तियों से।")),
            _lesson("h18", "How Lovely the World Is", "दुनिया कितनी प्यारी है",
                    ("Noticing the world around us", "Notice beautiful things nearby and describe their colours, sounds or shapes. Respect nature and living things.", "Find three lovely things near home or school and talk about them.", "Name one lovely thing around you.", "Any suitable answer."),
                    ("अपने आसपास की दुनिया", "आसपास की सुंदर चीज़ों को ध्यान से देखें और उनके रंग, आवाज़ या आकार बताएं। प्रकृति और जीवों का आदर करें।", "घर या स्कूल के आसपास की तीन अच्छी चीज़ें देखें और उनके बारे में बोलें।", "अपने आसपास की एक सुंदर चीज़ का नाम बताइए।", "कोई भी उपयुक्त उत्तर।")),
            _lesson("h19", "The Moon's Child", "चाँद का बच्चा",
                    ("Imagination and night-sky words", "Notice imagination in poems and stories. Name things that can be seen in the night sky.", "Draw the night sky and say an imaginative sentence about the moon.", "Can the moon be seen at night too?", "Yes, it can."),
                    ("कल्पना और रात के आकाश के शब्द", "कविता और कहानी में कल्पना पहचानें। रात के आकाश में दिखाई देने वाली चीज़ों के नाम बताएं।", "रात के आकाश का चित्र बनाएँ और चाँद के बारे में एक कल्पनापूर्ण वाक्य बोलें।", "चाँद दिन में दिखता है या रात में भी दिख सकता है?", "रात में भी दिख सकता है।")),
        ),
    ),
}
