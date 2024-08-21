from enum import Enum


class SupportedLanguages(Enum):
    RU = 'RU'
    EN = 'EN'


error_descriptions = {}

error_descriptions[SupportedLanguages.RU] = {
    "PARSE_ERROR": {
        "msg": "Ошибка при разборе LaTeX-кода. Возможно, где-то не закрыта формула знаком доллара, либо наоборот забыт доллар перед формулой.",
        "severity": 0
    },
    "DOUBLE_DOLLARS": {
        "msg": "Двойных долларов в тексте быть не должно. Выносные формулы нужно оформлять с помощью <code>\\[</code>…<code>\\]</code>. Объяснение <a href=\"https://tex.stackexchange.com/questions/503/why-is-preferable-to\" target=\"_blank\">по ссылке</a>.",
        "severity": 0
    },
    "CONSECUTIVE_DISPLAY_FORMULAE": {
        "msg": "Обнаружены две идущие подряд выключные формулы. Такого быть не должно: используйте окружение <code>aligned</code> или его аналоги, чтобы грамотно оформить не умещающиеся на одной строке выкладки. Подробнее, например, по <a href=\"https://www.overleaf.com/learn/latex/Aligning_equations_with_amsmath\" target=\"_blank\">ссылке</a>.",
        "severity": 0
    },
    'LINEBREAK_AFTER_DISPLAY_FORMULAE': {
        "msg": "Обнаружен разрыв строки непосредственно рядом с выключной формулой. После выключной формулы переход на новую строку выполняется автоматически. Если Вы хотели увеличить отступ по вертикали до следующего за формулой текста, используйте другие средства.",
        "severity": 0
    },
    'LINEBREAK_BEFORE_DISPLAY_FORMULAE': {
        "msg": "Обнаружен разрыв строки непосредственно перед выключной формулой. Перед выключной формулой переход на новую строку выполняется автоматически. Если Вы хотели увеличить отступ по вертикали между текстом и формулой.",
        "severity": 0
    },
    "EQNARRAY_USED": {
        "msg": "Не используйте окружение <code>eqnarray</code> (подробности по <a href=\"https://tex.stackexchange.com/a/197\" target=\"_blank\">ссылке</a>). Вместо этого пользуйтесь, например, <code>align</code>.",
        "severity": 0
    },
    "ABBREVIATIONS_WITH_SPACE": {
        "msg": "Сокращения типа <em>т.&thinsp;е.</em>, <em>т.&thinsp;к.</em>, <a href=\"https://ru.wikipedia.org/wiki/Q.E.D.\" target=\"_blank\"><em>ч.&thinsp;т.&thinsp;д.</em></a> и подобные <a href=\"https://new.gramota.ru/spravka/buro/search-answer?s=296030\">следует оформлять с пробелом</a> (см. также <a href=\"https://popravilam.com/blog/105-probel-v-sokrashcheniyah.html\" target=\"_blank\">тут</a>), но есть особенность: использовать нужно <em>неразрывный</em> пробел <code>~</code> или, ещё лучше, <a href=\"https://ru.wikipedia.org/wiki/%D0%A3%D0%B7%D0%BA%D0%B8%D0%B9_%D0%BF%D1%80%D0%BE%D0%B1%D0%B5%D0%BB\" target=\"_blank\"><em>тонкую шпацию</em></a> <code>\\,</code> — это неразрывный пробел несколько меньшей ширины, нежели обычный. Например: <code>ч.\\,т.\\,д.</code>. В противном случае может случиться казус при переносе текста, когда часть сокращения останется на строке, а часть перейдёт на следующую. Тонкая шпация также смотрится лучше в этом случае, чем обычный пробел. Также её используют при наборе <a href=\"https://new.gramota.ru/spravka/letters/78-init\" target=\"_blank\">инициалов</a>, например: <code>М.\\,В.~Ломоносов</code> или <code>М.\\,В.\\,Ломоносов</code>.",
        "severity": 0
    },
    "DASH_HYPHEN": {
        "msg": "Возможно, перепутано тире с дефисом. Полноценное длинное тире ставится с помощью <code>---</code>, укороченное с помощью <code>--</code>. Подробнее о тире, дефисах и подобном см. <a href=\"https://webstyle.sfu-kras.ru/tire-defis\" target=\"_blank\">здесь</a> и <a href=\"https://habrahabr.ru/post/20588/\" target=\"_blank\">здесь</a>. Ну и, конечно, никогда не поздно почитать <a href=\"https://www.artlebedev.ru/kovodstvo/sections/97/\" target=\"_blank\">А. Лебедева</a>.",
        "severity": 0
    },
    "DASH_IN_MATH_MODE": {
        "msg": "Похоже, Вы хотели поставить дефис. Но когда знак дефиса попадает в математический режим, он становится минусом. Вывод: делать дефис не частью формулы, а частью следующего за ней текста.",
        "severity": 0
    },
    "DASH_SURROUND_WITH_SPACES": {
        "msg": "Тире с двух сторон следует окружать пробелами. Особенный шик — один или оба из пробелов сделать неразрывными, чтобы тире не «повисало на краю пропасти» при переносе строки. Подробнее о тире, дефисах и подобном см. <a href=\"https://webstyle.sfu-kras.ru/tire-defis\" target=\"_blank\">здесь</a> и <a href=\"https://habrahabr.ru/post/20588/\" target=\"_blank\">здесь</a>. Ну и, конечно, никогда не поздно почитать <a href=\"https://www.artlebedev.ru/kovodstvo/sections/97/\" target=\"_blank\">А. Лебедева</a>.",
        "severity": 0
    },
    "RU_ORDINAL_ABBREVIATION": {
        "msg": "Нарушены <a href=\"https://new.gramota.ru/spravka/letters/22-spravka/letters/87-rubric-99\" target=\"_blank\">правила сокращения порядковых числительных</a>.",
        "severity": 0
    },
    "PARAGRAPH_BREAK_BEFORE_DISPLAY_FORMULA": {
        "msg": "Пустая строка заставляет \\(\\LaTeX\\) начинать новый параграф, даже если эта пустая строка стоит прямо перед выключной формулой. Чаще всего это не нужно, так как параграфы по смыслу не следует начинать с формул, а выключную формулу \\(\\LaTeX\\) в любом случае окаймляет достаточным количеством пустого пространства.",
        "severity": 0
    },
    "UNNECESSARY_FORMULA_BREAK": {
        "msg": "Возможно, некоторые формулы следовало объединить. Например, вместо <code>$x$, $y$ $\\in$ $A$</code> пишите <code>$x,\\,y\\in A$</code>; вместо <code>$a$ = $b+c$</code> пишите <code>$a=b+c$</code> и т.д.",
        "severity": 0
    },
    "CENTERING": {
        "msg": "Центрирование явно используется только при включении рисунков и таблиц. Иногда для заголовков. Для обычных формул центрирование не используется, вместо этого следует делать выключные формулы.",
        "severity": 0
    },
    "LOW_LEVEL_FONT_COMMANDS": {
        "msg": "Вместо низкоуровневых команд <code>{\\it …}</code>, <code>{\\bf …}</code> используйте команды <code>\\textit{…}</code> <code>\\textbf{…}</code> (подробности см. по <a href=\"https://tex.stackexchange.com/questions/41681/correct-way-to-bold-italicize-text\" target=\"_blank\">ссылке</a>.) Кроме того, выделять текст лучше не курсивом, а более гибкой командой <code>\\emph{…}</code>, поскольку она корректно сработает даже внутри курсивного блока.",
        "severity": 0
    },
    "WRONG_QUOTES": {
        "msg": "Для закавычивания слов «клавиатурные» кавычки <code>\"…\"</code> в \\(\\LaTeX\\) не используются. Если нужно закавычить слово, делайте это одним из способов <code>``…''</code> (два апострофа на букве ё вначале и два на букве э в конце) или <code><<…>></code> (два знака меньше и два знака больше).",
        "severity": 0
    },
    "WRONG_SAME_QUOTES": {
        "msg": "Открывающие и закрывающие кавычки ставятся по-разному: непривильно делать <code>''…''</code> или <code>``…``</code>, следует делать <code>``…''</code> для закавычивания в англоязычном тексте. В русской типографике применяются французские <code><<кавычки-ёлочки>></code>, для вложенных кавычек — немецкие <code>,,кавычки-лапки``</code>.",
        "severity": 0
    },
    "QUOTES_IN_MATH": {
        "msg": "Обнаружен символ кавычки в математическом режиме. Если Вы хотели поставить двойной штрих над математическим символом, наберите два штриха подряд: <code>y''</code>, либо используйте команду <code>\\prime\\prime</code>.",
        "severity": 0
    },
    "LATIN_LETTER_OUTSIDE_MATH_RU": {
        "msg": "Даже одна буква, если у неё математический смысл (если это имя математического объекта) — должна быть набрана в математическом режиме.",
        "severity": 0
    },
    "MATH_SEMANTICS_OUTSIDE_MATH": {
        "msg": "Команды, печатающие символы, имеющие математическую природу, настоятельно рекомендуется использовать в математическом режиме, даже если они работают и без оного.",
        "severity": 0
    },
    "LATIN_LETTER_C_MISUSED": {
        "msg": "Возможно, использована случайно латинская буква с (це) вместо русского предлога <strong>с</strong> посреди текста на русском языке.",
        "severity": 0
    },
    "CYRILLIC_LETTER_C_MISUSED": {
        "msg": "Возможно, использована случайно одна из кириллических букв <strong>а</strong>, <strong>е</strong>, <strong>с</strong>, <strong>х</strong> вместо соответствующей латинской буквы внутри формулы.",
        "severity": 0
    },
    "MULTIPLICATION_SIGN": {
        "msg": "Знак <code>*</code> используется для обозначения умножения в программировании, но не в математике. Пользуйтесь командой <code>\\cdot</code> или <code>\\times</code> (последней только в особых случаях).",
        "severity": 0
    },
    "SPACE_BEFORE_PUNCTUATION_MARK": {
        "msg": "Пробелы перед двоеточием, запятой, точкой, восклицательным и вопросительными знаками, точкой с запятой не ставятся.",
        "severity": 0
    },
    "SPACE_BEFORE_PARENTHESIS": {
        "msg": "В тексте перед открывающей скобкой ставится пробел.",
        "severity": 0
    },
    "SPACE_AFTER_PUNCTUATION_MARK": {
        "msg": "После двоеточия, запятой, точки, точки с запятой, восклицательного и вопросительного знаков нужно ставить пробел.",
        "severity": 0
    },
    "SPACE_AFTER_PARENTHESIS": {
        "msg": "После открывающей скобки не следует ставить пробел.",
        "severity": 0
    },
    "CAPITALIZATION_AFTER_PUNCTUATION_MARK": {
        "msg": "После двоеточия, точки с запятой, запятой, — не должно должно быть заглавной буквы, поскольку предложение продолжается.",
        "severity": 0
    },
    "CAPITALIZATION_AFTER_PERIOD": {
        "msg": "Предложение следует начинать с заглавной буквы.",
        "severity": 0
    },
    "PERIOD_BEFORE_NEXT_SENTENCE": {
        "msg": "В конце предложения должна ставиться точка, даже если предложение заканчивается формулой.",
        "severity": 0
    },
    "LEFT_RIGHT_RECOMMENDED": {
        "msg": "Когда при наборе формул возникает необходимость поставить скобки (круглые/фигурные/квадратные) или знак модуля вокруг высокой подформулы (дроби, биномиального коэффициента, суммы с пределами), рекомендуется добавлять команды <code>\\left</code> и <code>\\right</code>. Особенно это актуально для выключных формул. Например, сравните, как нелепо выглядит в PDF скомпилированная формула <code>\\[(\\frac{a}{b})^2\\]</code> и как естественен её «правильный» вариант <code>\\[\\left(\\frac{a}{b}\\right)^2\\]</code>. Тем не менее, переусердствовать здесь тоже не стоит: добавляйте <code>\\left… … \\right…</code> только тогда, когда видите явное несоответствие между высотой скобок и высотой того, что они окружают. Подробности по <a href=\"https://tex.stackexchange.com/a/58641\" target=\"_blank\">ссылке</a>. Можно также воспользоваться командой <a href=\"https://tex.stackexchange.com/a/1765\" target=\"_blank\"><code>\\DeclarePairedDelimiter</code></a> из библиотеки mathtools.",
        "severity": 10
    },
    "SYMBOLIC_LINKS": {
        "msg": "Пользуйтесь символическими ссылками, например: <code>Заметим, что \\begin{equation}\\label{eqSquares} a^2-b^2=(a-b)(a+b). \\end{equation} Из равенства~\\eqref{eqSquares}, следует, что…</code>.",
        "severity": 0
    },
    "EQREF_INSTEAD_OF_REF": {
        "msg": "Вместо <code>(\\ref{…})</code> следует писать <code>\\eqref{…}</code>",
        "severity": 0
    },
    "NONBREAKABLE_SPACE_BEFORE_REF": {
        "msg": "Перед командами <code>\\ref</code>, <code>\\eqref</code> рекомендуется ставить тильду, чтобы номер ссылки был приклеен неразрывным пробелом, например: <code>…Согласно~\\eqref{eqMaxwell}, имеем…</code>.",
        "severity": 0
    },
    "ELLIPSIS_LDOTS": {
        "msg": "В математическом режиме многоточие ставится не <code>...</code>, а командой <code>\\ldots</code>, а в текстовом режиме — командой <code>\\textellipsis</code>. При наличии пакета amsmath, когда многоточие нужно вставить между запятыми в перечислении объектов, используйте команду <code>\\dotsc</code>.",
        "severity": 0
    },
    "TRIVIAL_LABEL": {
        "msg": "Символические ссылки нужно делать, но нет большого смысла делать тривиальные описания типа <code>\\label{eq1}</code>. Так же, как в программировании называть переменную <code>var1</code> чаще всего пагубно. Куда лучше придумать осмысленное название, например <code>eqCauchy</code>, <code>eqBinomialSymmetry</code>, <code>eqMain</code> (если это действительно самая важная формула в доказательстве) и т.д.",
        "severity": 5
    },
    "REPLACE_MBOX_WITH_TEXT": {
        "msg": "Для вставки текста внутрь формулы вместо команд <code>\\mbox</code> и <code>\\hbox</code> пользуйтесь командой <code>\\text</code>. Объяснение см. по <a href=\"https://tex.stackexchange.com/questions/70632/difference-between-various-methods-for-producing-text-in-math-mode\" target=\"_blank\">ссылке</a>.",
        "severity": 0
    },
    "TEXT_IN_MATH_MODE": {
        "msg": "Для вставки текста внутрь формулы (даже если слова на латинице, но не являются именами математических объектов) вместо команд пользуйтесь командой <code>\\text</code>, например: <code>Рассмотрим множество $A_{\\text{хорошие}}$</code>.",
        "severity": 0
    },
    "INCORPORATE_NOT": {
        "msg": "Хотя префикс <code>\\not</code> позволяет из многих значков получить значок-отрицание, часто короче (и <a href=\"https://tex.stackexchange.com/a/141011\" target=\"_blank\">рекомендуется</a>!) писать одной командой. Например, вместо <code>\\not=</code> можно написать <code>\\ne</code>, вместо <code>\\not\\in</code> написать <code>\\notin</code> и т.д.",
        "severity": 0
    },
    "OVER_VS_FRAC": {
        "msg": "Команда <code>\\over</code> является низкоуровневой командой TeX и <a href=\"https://tex.stackexchange.com/a/73825\" target=\"_blank\">не рекомендуется</a> к использованию в \\(\\LaTeX\\). Вместо <code>A \\over B</code> пишите <code>\\frac{A}{B}</code>.",
        "severity": 0
    },
    "CHOOSE_VS_BINOM": {
        "msg": "Команда <code>\\choose</code> является низкоуровневой командой TeX и <a href=\"https://tex.stackexchange.com/a/127711\" target=\"_blank\">не рекомендуется</a> к использованию в \\(\\LaTeX\\). Вместо <code>A \\choose B</code> пишите <code>\\binom{A}{B}</code>.",
        "severity": 0
    },
    "SETS_IN_BBFONT": {
        "msg": "Стандартные числовые множества (натуральные числа и пр.) нужно набирать специальным шрифтом: вместо <code>N</code> пишите <code>\\mathbb{N}</code>.",
        "severity": 0
    },
    "MOD_NOT_A_COMMAND": {
        "msg": "Используйте команду <code>\\bmod</code> или <code>\\pmod</code>, чтобы mod был набран в формуле прямым шрифтом (как и подобает операции, а не произведению трёх переменных m, o и d).",
        "severity": 0
    },
    "TILDE_INEFFECTIVE_AS_NBSP": {
        "msg": "Значок <code>~</code> означает неразрывный пробел. Окружать его пробелами бессмысленно: неразрывность пропадает. Например, вместо <code>По формуле ~\\eqref{…</code> следует писать <code>По формуле~\\eqref{…</code>",
        "severity": 0
    },
    "INDENTATION_WITH_SPACES": {
        "msg": "Избегайте использования нескольких пробельных значков подряд, так же, как и в WYSIWYG-редакторах не следует делать отступы множественными пробелами. Выберите <em>одну</em> подходящую команду \\(\\LaTeX\\) для отступа в конкретной ситуации, подробности по <a href=\"https://tex.stackexchange.com/a/74354\" target=\"_blank\">ссылке</a>.",
        "severity": 0
    },
    "LE_AS_SINGLE_COMMAND": {
        "msg": "Чтобы набрать символ \\(\\le\\) или \\(\\ge\\), используйте команды <code>\\le</code> и <code>\\ge</code> соответственно. Стрелка \\(\\Leftarrow\\) набирается командой <code>\\Leftarrow</code>. Программистские сочетания <code><=</code> и <code>>=</code> ни в одной из ситуаций не годятся.",
        "severity": 0
    },
    "PUNCTUATION_AFTER_DISPLAY_MATH": {
        "msg": "Если поставить знак препинания после выключной формулы, он будет отображён на другой строке. Поэтому при необходимости поставить, например, запятую сразу после выключной формулы, запятую следует сделать частью этой формулы.",
        "severity": 0
    },
    "BACKSLASH_NEEDED": {
        "msg": "Слова \\(\\min\\), \\(\\max\\) и подобные в формулах являются именами математических операторов и должны набираться прямым шрифтом. В \\(\\LaTeX\\) есть команды <code>\\min</code>, <code>\\max</code>, <code>\\lim</code>, <code>\\deg</code>, и другие, которые делают эту работу за Вас. Список доступных стандартных команд см. по <a href=\"https://www.overleaf.com/learn/latex/Operators#Reference_guide\" target=\"_blank\">ссылке</a>. Если такой команды ещё нет, используйте конструкцию типа <code>\\operatorname{min}</code> или, ещё лучше, <a href=\"https://tex.stackexchange.com/a/67529\" target=\"_blank\">создайте свой оператор</a> командой <code>\\DeclareMathOperator</code> в преамбуле документа.",
        "severity": 0
    },
    "CDOT_FOR_READABILITY": {
        "msg": "В произведениях чисел, обозначаемых отдельной буквой, и дробей или биномиальных коэффициентов, полезно для улучшения читабельности текста явно указывать произведение командой <code>\\cdot</code>.",
        "severity": 5
    },
    "GRAPHICS_IN_MATH_MODE": {
        "msg": "Команда <code>\\includegraphics</code> не должна использоваться в математическом режиме без <em>крайней</em> необходимости. Чтобы отцентрировать рисунок, вместо помещения рисунка в выключную формулу используйте окружения <code>center</code> и <code>figure</code>.",
        "severity": 0
    },
    "UNNECESSARY_MATH_MODE": {
        "msg": "Если внутри формулы (в окружении долларов) стоит единственный символ и он не является буквой или цифрой — это тревожный знак. Скорее всего, либо в математический режим переходить было не нужно, либо без нужды на части была разорвана формула.",
        "severity": 0
    },
    "NO_SPACE_AFTER_COMMAND_BEFORE_CYRILLIC": {
        "msg": "Хотя \\(\\LaTeX\\) это и не считает ошибкой, не следует писать слитно команды ТеХа и кириллические слова.",
        "severity": 0
    },
    "TEXT_COMMANDS_IN_MATH_MODE": {
        "msg": "Текстовые команды <code>\\textbf</code>, <code>\\textit</code> не следует использовать в математическом режиме. Для набора жирным шрифтом математических символов есть команда <code>\\mathbf</code>.",
        "severity": 0
    },
    "LIMITS_UNNECESSARY_IN_DISPLAY_MODE": {
        "msg": "Команда <code>\\limits</code> в выключных формулах обычно лишняя: пределы и без неё выставляются верно.",
        "severity": 0
    },
    "FORMULA_NEIGHBOURING_REFERENCE": {
        "msg": "Плохо читается, когда формула непосредственно соседствует со ссылкой, без знаков препинания. Всегда можно вставить слово либо поменять порядок слов в предложении, чтобы этого избежать.",
        "severity": 0
    },
    "UNICODE_SQRT": {
        "msg": "Для квадратного корня следует использовать команду <code>\\sqrt</code> вместо символа Unicode.",
        "severity": 0
    },
    "NUMBERED_MATH_NEEDS_REFERENCING": {
        "msg": "Если у формулы есть видимый номер, то этот номер должен быть использован где-то в тексте для ссылки на формулу. А если на формулу необязательно ссылаться, то и нумеровать её не следует.",
        "severity": 0
    },
    # todo
    "NO_CONCLUSION": {
        "msg": "Обычно решение задачи или доказательство теоремы не заканчивают рисунком или формулой. Полезно добавить в конце хотя бы какое-то заключение, например: <code>Теорема доказана.</code>, <code>В итоге мы получили ответ: искомое количество равно $42$.</code> и т.д.",
        "severity": 5
    },
    "SUGGESTED_NEW_PARAGRAPH": {
        "msg": "Чтобы начать с новой строки формулу, она делается выключной. Чтобы начать новый параграф текста, используется команда <code>\\par</code> в текстовом режиме. Использовать же несемантичный перенос <code>\\\\</code>, помимо окружений типа <code>tabular</code>, следует только в крайних случаях.",
        "severity": 0
    },
    "NUMERALS_AS_WORDS": {
        "msg": "Со стилистической точки зрения, числительные, не превосходящие пяти и окружённые текстом, часто лучше писать не цифрами, а словами. Например, <em>Рассмотрим 2 случая</em> смотрится хуже, чем <em>Рассмотрим два случая</em>.",
        "severity": 10
    },
    "MID_IN_SET_COMPREHENSION": {
        "msg": "При описании множеств вертикальная черта ставится командой <code>\\mid</code>. Например, <code>\\{x^2\\mid x\\in\\mathbb{Z}\\}</code>. И, наоборот, <code>\\mid</code> НЕ используется в остальных контекстах, например, при обозначении модуля числа. Для обозначения последнего пишите <code>|x|</code> или <code>\\lvert x \\rvert</code>.",
        "severity": 0
    },
    # todo
    "FLOOR_FUNCTION_NOTATION": {
        "msg": "В современной литературе принято целую часть числа \\(x\\) обозначать <code>\\lfloor x\\rfloor</code>, а не <code>[x]</code>.",
        "severity": 0
    },
    "ITALIC_INSTEAD_OF_EMPH": {
        "msg": "Выделять текст лучше не курсивом, а более гибкой командой <code>\\emph{…}</code>, поскольку она корректно сработает даже внутри курсивного блока.",
        "severity": 0
    },
    # todo
    "PARAGRAPH_STARTS_WITH_FORMULA": {
        "msg": "Параграф не следует начинать с формулы. Если Вы хотите, чтобы формула была на отдельной строке, а не в тексте, сделайте её выносной: <code>\\[…\\]</code>.",
        "severity": 0
    },
    # todo
    "SENTENCE_STARTS_WITH_FORMULA": {
        "msg": "Обычно предложение не следует начинать с формулы. Почти всегда можно добавить в начало слово. Например, вместо предложения <code>$G$ связен.</code> напишите <code>Граф $G$ связен.</code>",
        "severity": 0
    },
    # todo
    "SENTENCE_STARTS_WITH_NUMBER": {
        "msg": "Обычно предложение не следует начинать с цифровой записи числа. Например, вместо предложения <code>5 человек можно выстроить в очередь $5!$ способами.</code> лучше написать либо <code>Пятерых человек…</code> либо <code>Заметим, что 5 человек…</code>",
        "severity": 5
    },
    # todo
    "RUSSIAN_TYPOGRAPHY_PECULIARITIES": {
        "msg": "Строго говоря, это не является ошибкой, но в отечественной типографской традиции принято пустое множество обозначать значком <code>\\varnothing</code>, а не <code>\\emptyset</code> (последний более приплюснутый). Аналогично, вместо <code>\\epsilon</code> лучше писать <code>\\varepsilon</code>, а вместо <code>\\phi</code> писать <code>\\varphi</code>.",
        "severity": 0
    },
    # todo
    "BETTER_TO_USE_WORDS_THEN_MATH": {
        "msg": "Конструкции наподобие <code>число элементов $=m^2$</code> недопустимы в письменном тексте, за исключением конспектов. Знаки \\(=, \\gt, \\geqslant\\) и др. нужно в этих случаях писать словами: <code>…не превосходит $m^2$</code>, <code>…равняется $m^2$</code> и т.д.",
        "severity": 0
    },
    # todo
    "MATH_ENVIRONMENT_VERBOSITY_WARNING": {
        "msg": "Окружение <code>math</code> используется довольно редко. Лучше всего вместо него использовать более короткую (и абсолютно такую же по получаемому результату) конструкцию <code>\\(…\\)</code> или <code>$…$</code>. Часто также ошибочно полагают, что с помощью math оформляют <em>выключные</em> формулы — но это не так: внутри окружения math действует обычный inline-режим. Для оформления выключных формул подойдёт либо конструкция <code>\\[…\\]</code>, либо одно из окружений equation, array и др.",
        "severity": 0
    },
    # todo
    "USE_DIVIDES_INSTEAD_OF_VDOTS": {
        "msg": "Команду <code>\\vdots</code> следует использовать только в матрицах или похожих окружениях для обозначения именно многоточия по вертикали. Когда речь идёт о делимости, вместо трёх точек (в качестве слов «делится на») используйте вертикальную черту (в качестве слов «является делителем»). Когда же рядом ещё вертикальные черта, например, в set builder notation, разумно вообще писать словами: <code>\\( A=\\{x\\in\\mathbb{N} \\mid x\\text{ кратен } 5\\} \\)</code>",
        "severity": 0
    },
    # todo
    "MAKE_LONG_FORMULA_DISPLAY": {
        "msg": "Подозрительно длинная формула набрана не в выключном режиме. Формулы, которые при компиляции не влезают целиком на одну строку (т.е. вся строка занята формулой и всё равно возникает перенос), нужно делать выключными, аккуратно их разбивая построчно с помощью окружений AMS: см. перечень подходящих окружений в <a href=\"https://www.overleaf.com/learn/latex/Aligning_equations_with_amsmath\" target=\"_blank\">документе по ссылке</a>.",
        "severity": 0
    },
    # todo
    "EN_ORDINAL_ABBREVIATION": {
        "msg": "",
        "severity": 0
    },
    # todo
    "LATE_DEFINITION": {
        "msg": "Вместо того, чтобы писать <q><code>$x=a+b$</code>, где <code>$a=…</code></q> сначала лучше ввести все буквы и лишь затем записать выражение, эти буквы содержащие. См. <a href=\"https://1drv.ms/w/s!AiAwrmxQ9QLrjOtTQqAXWdl3ryK5Jg?e=vEMU6W\" target=\"_blank\">статью П. Халмоша</a>, раздел «Правильно используйте слова».",
        "severity": 0
    },
    # todo
    "INVISIBLE_BRACES": {
        "msg": "Чтобы вывести на экран фигурные скобки, нужно написать <code>\\{…\\}</code>. Если писать просто <code>{…}</code>, скобки играют роль не символов, а «объединителей» TeX-овских команд. Кстати, в роли объединителей ими не нужно злоупотреблять; используйте их только при необходимости.",
        "severity": 0
    },
    # todo
    "MANUAL_LISTS": {
        "msg": "Не следует вручную создавать нумерованные списки. Пишите так: <code>\\begin{enumerate}\\item Во-первых, \\item Во-вторых … \\end{enumerate}</code>. Подробнее об оформлении списков в \\(\\LaTeX\\) можно прочитать, например, <a href=\"https://www.overleaf.com/learn/latex/Lists\" target=\"_blank\">здесь</a>.",
        "severity": 0
    }
}

error_descriptions[SupportedLanguages.EN] = {
    "PARSE_ERROR": {
        "msg": "Error parsing LaTeX code. Possibly, a formula is not closed with a dollar sign somewhere, or conversely, a dollar is forgotten before a formula.",
        "severity": 0
    },
    "DOUBLE_DOLLARS": {
        "msg": "Double dollars for display math should be avoided in \\(\\LaTeX\\). Use <code>\\[</code>\u2026<code>\\]</code> for display style formulas. See <a href=\"https://tex.stackexchange.com/questions/503/why-is-preferable-to\" target=\"_blank\">explanation</a>.",
        "severity": 0
    },
    "CONSECUTIVE_DISPLAY_FORMULAE": {
        "msg": "Two consecutive display style formulas have been detected. This should be avoided. Use <code>aligned</code> environment or its analogues to properly typeset long formula that does not fit into single line. See e.g. <a href=\"https://www.overleaf.com/learn/latex/Aligning_equations_with_amsmath\" target=\"_blank\">these guidelines</a>.",
        "severity": 0
    },
    "LINEBREAK_AFTER_DISPLAY_FORMULAE": {
        "msg": "Line break detected immediately next to a display formula. After a display formula, the transition to a new line is automatic. If you wanted to increase the vertical spacing to the next text after the formula, use other means.",
        "severity": 0
    },
    "LINEBREAK_BEFORE_DISPLAY_FORMULAE": {
        "msg": "Line break detected immediately before a display formula. Before a display formula, the transition to a new line is automatic. If you wanted to increase the vertical spacing between the text and the formula.",
        "severity": 0
    },
    "EQNARRAY_USED": {
        "msg": "Avoid <code>eqnarray</code> environment (see <a href=\"https://tex.stackexchange.com/a/197\" target=\"_blank\">details</a>). Use e.g. <code>align</code> instead.",
        "severity": 0
    },
    "ABBREVIATIONS_WITH_SPACE": {
        "msg": "Abbreviations like <em>i.&thinsp;e.</em>, <em>e.&thinsp;g.</em>, <a href=\"https://en.wikipedia.org/wiki/Q.E.D.\" target=\"_blank\"><em>q.&thinsp;e.&thinsp;d.</em></a> and similar should be formatted with a space, but there is a peculiarity: it is necessary to use a <em>non-breaking</em> space <code>~</code> or, even better, <a href=\"https://en.wikipedia.org/wiki/Thin_space\" target=\"_blank\"><em>thin space</em></a> <code>\\,</code> \u2014 this is a non-breaking space slightly narrower than the usual one. For example: <code>q.\\,e.\\,d.</code>. Otherwise, a case may occur during text wrap when part of the abbreviation remains on the line and part moves to the next. Thin space also looks better in this case than a regular space. It is also used when typing initials, for example: <code>J.\\,D.~Smith</code> or <code>J.\\,D.\\,Smith</code>.",
        "severity": 0
    },
    "DASH_HYPHEN": {
        "msg": "Looks like you have wrongly used hyphen instead of dash. You can typeset M-dash \u201c\u2014\u201d with <code>---</code> and N-dash \u201c\u2013\u201d with <code>--</code> in \\(\\LaTeX\\). See <a href=\"https://www.grammarly.com/blog/hyphens-and-dashes/\" target=\"_blank\">details</a>.",
        "severity": 0
    },
    "DASH_IN_MATH_MODE": {
        "msg": "Looks like you wanted to typeset a hyphen. But when hyphen appears in math mode \\(\\LaTeX\\) treats it as minus. So you should make this hyphen part of the text that follows the formula, not the formula itself.",
        "severity": 0
    },
    "DASH_SURROUND_WITH_SPACES": {
        "msg": "An em dash should be surrounded by spaces on both sides. A particularly chic look is achieved by making one or both of these spaces non-breaking, so the em dash does not 'hang on the edge of the abyss' during line breaks.",
        "severity": 0
    },
    "RU_ORDINAL_ABBREVIATION": {
        "msg": "Rules for abbreviating ordinal numbers are violated <a href=\"https://new.gramota.ru/spravka/letters/22-spravka/letters/87-rubric-99\" target=\"_blank\">here</a>.",
        "severity": 0
    },
    "PARAGRAPH_BREAK_BEFORE_DISPLAY_FORMULA": {
        "msg": "An empty line makes \\(\\LaTeX\\) to start a new paragraph even if this line happens just before a display-style formula. Most of the time it is not needed, as paragraphs should not start with formulae, and as display math already have enough space before and after.",
        "severity": 0
    },
    "UNNECESSARY_FORMULA_BREAK": {
        "msg": "Looks like some math needs concatenating. For instance, instead of <code>$x$, $y$ $\\in$ $A$</code> write <code>$x,\\,y\\in A$</code>; instead of <code>$a$ = $b+c$</code> write <code>$a=b+c$</code> etc.",
        "severity": 0
    },
    "CENTERING": {
        "msg": "Explicit centering should only be used in figure an table environments, and sometimes for headings. Avoid centering of non-display-style formulae.",
        "severity": 0
    },
    "LOW_LEVEL_FONT_COMMANDS": {
        "msg": "Instead of using low-level TeX commands <code>{\\it \u2026}</code>, <code>{\\bf \u2026}</code>. Instead use <code>\\textit{\u2026}</code>, <code>\\textbf{\u2026}</code> etc (see <a href=\"https://tex.stackexchange.com/questions/41681/correct-way-to-bold-italicize-text\" target=\"_blank\">details</a>.) It is also recommended to use <code>\\emph{\u2026}</code> command to emphasize portions of the text instead of italicizing, as it nicely works also inside italicized text blocks.",
        "severity": 0
    },
    "WRONG_QUOTES": {
        "msg": "Do not use \u201cprogrammers\u2019 quotes\u201d like <code>\"\u2026\"</code> to quote in \\(\\LaTeX\\). Use <code>``\u2026''</code> instead.",
        "severity": 0
    },
    "WRONG_SAME_QUOTES": {
        "msg": "Opening and closing quotes are usually different: avoid <code>''\u2026''</code> or <code>``\u2026``</code>, make it <code>``\u2026''</code> instead.",
        "severity": 0
    },
    "QUOTES_IN_MATH": {
        "msg": "Quote symbol detected in math mode. If you need to put a mathematical \u201cprime\u201d symbol use <code>\\prime\\prime</code> or just keyboard apostrophes <code>''</code>.",
        "severity": 0
    },
    "LATIN_LETTER_OUTSIDE_MATH_RU": {
        "msg": "Even one letter, if it has a mathematical meaning (if it is the name of a mathematical object) \u2014 should be typed in math mode.",
        "severity": 0
    },
    "MATH_SEMANTICS_OUTSIDE_MATH": {
        "msg": "Commands that typeset <em>mathematical</em> symbols should generally be placed inside math mode (in spite of some of them work in text mode also).",
        "severity": 0
    },
    "LATIN_LETTER_C_MISUSED": {
        "msg": "Looks like you have accidentally used latin c instead of cyrillic \u0441.",
        "severity": 0
    },
    "CYRILLIC_LETTER_C_MISUSED": {
        "msg": "Looks like you have accidentally used one of cyrillic letters a,e,c instead of their latin counterparts.",
        "severity": 0
    },
    "MULTIPLICATION_SIGN": {
        "msg": "Symbol <code>*</code> is used to denote multiplication in programming, not in mathematics. Use <code>\\cdot</code> or <code>\\times</code> instead (<code>\\times</code> is used only in special circumstances though).",
        "severity": 0
    },
    "SPACE_BEFORE_PUNCTUATION_MARK": {
        "msg": "There should be no space symbol inserted before colon, semicolon, comma, full stop, exclamation mark or question mark.",
        "severity": 0
    },
    "SPACE_BEFORE_PARENTHESIS": {
        "msg": "There should be a space before the opening parenthesis.",
        "severity": 0
    },
    "SPACE_AFTER_PUNCTUATION_MARK": {
        "msg": "There should be a space after colon, semicolon, comma, full stop, exclamation mark or question mark.",
        "severity": 0
    },
    "SPACE_AFTER_PARENTHESIS": {
        "msg": "There should be no space after the opening parenthesis.",
        "severity": 0
    },
    "CAPITALIZATION_AFTER_PUNCTUATION_MARK": {
        "msg": "Colon, semicolon, and comma do not mark the end of the sentence, and thus the word following them should generally not be capitalized.",
        "severity": 0
    },
    "CAPITALIZATION_AFTER_PERIOD": {
        "msg": "Sentences should start with capital letter.",
        "severity": 0
    },
    "PERIOD_BEFORE_NEXT_SENTENCE": {
        "msg": "Sentences should ultimately end with full stop even if they end with formula.",
        "severity": 0
    },
    "LEFT_RIGHT_RECOMMENDED": {
        "msg": "When in need of typesetting paired delimiters (parentheses, brackets, braces, absolute value symbol, norm symbol) around some large formula, it is recommended to add <code>\\left</code> and <code>\\right</code> commands. Compare how ugly is the PDF representation of a formula <code>\\[(\\frac{a}{b})^2\\]</code> and how beautiful is the proper variant of it: <code>\\[\\left(\\frac{a}{b}\\right)^2\\]</code>. On the other hand, <code>\\left\u2026 \u2026 \\right\u2026</code> should not be overused, use them just when you see the mismatch between the formula hight and the delimiter height. See <a href=\"https://tex.stackexchange.com/a/58641\" target=\"_blank\">details</a>. You can also employ <a href=\"https://tex.stackexchange.com/a/1765\" target=\"_blank\"><code>\\DeclarePairedDelimiter</code></a> command from <em>mathtools</em> library.",
        "severity": 10
    },
    "SYMBOLIC_LINKS": {
        "msg": "Employ symbolic cross-referencing, e.g.: <code>Note that \\begin{equation}\\label{eqSquares} a^2-b^2=(a-b)(a+b). \\end{equation} From~\\eqref{eqSquares} it follows that\u2026</code>. See <a href=\"https://www.overleaf.com/learn/latex/Cross_referencing_sections%2C_equations_and_floats\" target=\"_blank\">details</a>.",
        "severity": 0
    },
    "EQREF_INSTEAD_OF_REF": {
        "msg": "Write <code>\\eqref{\u2026}</code> instead of <code>(\\ref{\u2026})</code>.",
        "severity": 0
    },
    "NONBREAKABLE_SPACE_BEFORE_REF": {
        "msg": "Commands <code>\\ref</code>, <code>\\eqref</code> and such are recommended to be prepended with unbreakable space <code>~</code>, e.g.: <code>\u2026Using~\\eqref{eqMaxwell} we obtain\u2026</code>.",
        "severity": 0
    },
    "ELLIPSIS_LDOTS": {
        "msg": "You should use <code>\\ldots</code> for ellipsis in math mode instead of <code>...</code>. If you use <em>amsmath</em> package you can use <code>\\dotsc</code> command for ellipsis in typical mathematical enumerations.",
        "severity": 0
    },
    "TRIVIAL_LABEL": {
        "msg": "It is definitely a good idea to use symbolic cross-references instead of hard-coding explicit numbers, but you should avoid using non-semantic names of the references like <code>\\label{eq1}</code>. Just as a variable with the name <code>var1</code> is frowned upon in software development. Take time and think on some meaningful name, e.g. <code>eqCauchy</code>, <code>eqBinomialSymmetry</code>, <code>eqMain</code> (the latter if fine if this is indeed the most important formula in your proof) etc.",
        "severity": 5
    },
    "REPLACE_MBOX_WITH_TEXT": {
        "msg": "To place text inside a formula avoid using low-level <code>\\mbox</code> and <code>\\hbox</code> commands. Use <code>\\text</code> instead. See <a href=\"https://tex.stackexchange.com/questions/70632/difference-between-various-methods-for-producing-text-in-math-mode\" target=\"_blank\">details</a>.",
        "severity": 0
    },
    "TEXT_IN_MATH_MODE": {
        "msg": "To insert text inside a math formula use <code>\\text</code> command, e.g.: <code>Consider a set $A_{\\text{good}}$</code>.",
        "severity": 0
    },
    "INCORPORATE_NOT": {
        "msg": "Although <code>\\not</code> command does work to get a negated (crossed-out) sign, the <a href=\"https://tex.stackexchange.com/a/141011\" target=\"_blank\">better way</a> is to search for the dedicated command. For instance, <code>\\ne</code> is better than <code>\\not=</code>, <code>\\notin</code> is better than <code>\\not\\in</code> etc.",
        "severity": 0
    },
    "OVER_VS_FRAC": {
        "msg": "The command <code>\\over</code> is a low-level TeX command and <a href=\"https://tex.stackexchange.com/a/73825\" target=\"_blank\">should be avoided</a> in \\(\\LaTeX\\). Replace <code>A \\over B</code> with <code>\\frac{A}{B}</code>.",
        "severity": 0
    },
    "CHOOSE_VS_BINOM": {
        "msg": "The command <code>\\choose</code> is a low-level TeX command and <a href=\"https://tex.stackexchange.com/a/127711\" target=\"_blank\">should be avoided</a> in \\(\\LaTeX\\). Replace <code>A \\choose B</code> with <code>\\binom{A}{B}</code>.",
        "severity": 0
    },
    "SETS_IN_BBFONT": {
        "msg": "Standard number sets should be typeset in \u201cblackboard bold\u201d font: e.g. the usages of <code>N</code> as a set of naturals should be replaced with <code>\\mathbb{N}</code>.",
        "severity": 0
    },
    "MOD_NOT_A_COMMAND": {
        "msg": "Use <code>\\bmod</code> or <code>\\pmod</code> to typeset \\(\\bmod\\) with roman font.",
        "severity": 0
    },
    "TILDE_INEFFECTIVE_AS_NBSP": {
        "msg": "The symbol <code>~</code> denotes the unbreakable space in \\(\\LaTeX\\). It should not be surrounded with spaces: you loose unbreakability. For instance, instead of <code>Formula ~\\eqref{\u2026} implies\u2026</code> you should write <code>Formula~\\eqref{\u2026} implies\u2026</code>",
        "severity": 0
    },
    "INDENTATION_WITH_SPACES": {
        "msg": "Avoid using multiple spaces to indent text. Use proper \\(\\LaTeX\\) spacing command instead, see <a href=\"https://tex.stackexchange.com/a/74354\" target=\"_blank\">details</a>.",
        "severity": 0
    },
    "LE_AS_SINGLE_COMMAND": {
        "msg": "To typeset \\(\\le\\) or \\(\\ge\\) employ <code>\\le</code> and <code>\\ge</code> commands respectively. The arrow \\(\\Leftarrow\\) is typeset with <code>\\Leftarrow</code> command. Software developing combinations like <code><=</code> and <code>>=</code> are of no use in \\(\\LaTeX\\).",
        "severity": 0
    },
    "PUNCTUATION_AFTER_DISPLAY_MATH": {
        "msg": "When you place a punctuation mark right after a display-style formula, it is going to be thorn away from it and placed on a separate line (just look at the compiled PDF). So if you need e.g. to place a comma right after display formula, you should make this comma part of the formula itself.",
        "severity": 0
    },
    "BACKSLASH_NEEDED": {
        "msg": "Words \\(\\min\\), \\(\\max\\) and such in mathematical formulas are operator names and should be typeset with roman font. There are corresponding <em>commands</em> of \\(\\LaTeX\\) <code>\\min</code>, <code>\\max</code>, <code>\\lim</code>, <code>\\deg</code>, and others, that will do that work for you. See the list of these commands <a href=\"https://www.overleaf.com/learn/latex/Operators#Reference_guide\" target=\"_blank\">here</a>. If you cannot see the command that you need, write something like <code>\\operatorname{min}</code> or, even better, <a href=\"https://tex.stackexchange.com/a/67529\" target=\"_blank\">declare your own operator</a> with <code>\\DeclareMathOperator</code> command in the document preamble.",
        "severity": 0
    },
    "CDOT_FOR_READABILITY": {
        "msg": "When typesetting products of numbers, fractions, binomial coefficients and such, consider using explicit multiplication dot <code>\\cdot</code> occasionally.",
        "severity": 5
    },
    "GRAPHICS_IN_MATH_MODE": {
        "msg": "The <code>\\includegraphics</code> command should not be used in math mode except for you really know what you are doing with it. For instance, to center a figure on screen, use <code>center</code> and <code>figure</code> environments instead of surrounding your <code>\\includegraphics</code> with display math delimiters.",
        "severity": 0
    },
    "UNNECESSARY_MATH_MODE": {
        "msg": "If the only content of a formula is a single symbols which is neither a digit nor a single letter \u2014 that is suspicious! Most likely you either did not need math mode here or unnecessarily broke a formula into pieces.",
        "severity": 0
    },
    "NO_SPACE_AFTER_COMMAND_BEFORE_CYRILLIC": {
        "msg": "",
        "severity": 0
    },
    "TEXT_COMMANDS_IN_MATH_MODE": {
        "msg": "Text style commands <code>\\textbf</code>, <code>\\textit</code> and such should be avoided in math mode. There are math-mode commands for some font styles. For instance, <code>\\mathbf</code> for mathematical bold font.",
        "severity": 0
    },
    "LIMITS_UNNECESSARY_IN_DISPLAY_MODE": {
        "msg": "The <code>\\limits</code> command can be frequently omitted in display formulas: the operator limits are typically automatically placed above and below the operator even without it in display math mode.",
        "severity": 0
    },
    "FORMULA_NEIGHBOURING_REFERENCE": {
        "msg": "A formula that directly neighbours a reference typically looks inferior. You can always think on some word to insert in between them.",
        "severity": 0
    },
    "UNICODE_SQRT": {
        "msg": "To typeset the square root symbol use <code>\\sqrt</code> instead of UNICODE symbol. As a benefit, you will also get a beautiful stretching overline.",
        "severity": 0
    },
    "NUMBERED_MATH_NEEDS_REFERENCING": {
        "msg": "If a formula has a visible number, then this number must be used somewhere in the text to refer to the formula. And if it is not necessary to refer to the formula, then it should not be numbered.",
        "severity": 0
    },
    "NO_CONCLUSION": {
        "msg": "It is rarely a good idea to end the proof or a problem solution right on some formula or a figure. It is best to add some concluding remark in the end, e.g.: <code>This concludes the proof.</code> or <code>Thus we finally get unknown value: $42$.</code> etc.",
        "severity": 5
    },
    "SUGGESTED_NEW_PARAGRAPH": {
        "msg": "To place a formula on a new line you should make that formula to be display-style. To start a new paragraph use <code>\\par</code> in text mode. Avoid using low-level line break <code>\\\\</code> except for <code>tabular</code>, <code>matrix</code>, or similar environments.",
        "severity": 0
    },
    "NUMERALS_AS_WORDS": {
        "msg": "Stylistically it usually looks better when small numerals are kept as words, not numbers. E.g. <em>Consider 2 cases</em> looks inferior to <em>Consider two cases</em>.",
        "severity": 10
    },
    "MID_IN_SET_COMPREHENSION": {
        "msg": "When describing sets the vertical line is placed using <code>\\mid</code> command. E.g. <code>\\{x^2\\mid x\\in\\mathbb{Z}\\}</code>. In other contexts you should generally avoid <code>\\mid</code>. For instance, for absolute value use <code>|x|</code> or <code>\\lvert x \\rvert</code>.",
        "severity": 0
    },
    "FLOOR_FUNCTION_NOTATION": {
        "msg": "In modern mathematical literature the integer part of number \\(x\\) is denoted as <code>\\lfloor x\\rfloor</code>, not <code>[x]</code>.",
        "severity": 0
    },
    "ITALIC_INSTEAD_OF_EMPH": {
        "msg": "Consider using <code>\\emph{\u2026}</code> for text emphasis instead of italicizing, as it nicely works also inside italicized text blocks.",
        "severity": 0
    },
    "PARAGRAPH_STARTS_WITH_FORMULA": {
        "msg": "A paragraph should not start with a formula. If you need to place a formula on a separate line, typeset it in display mode using <code>\\[\u2026\\]</code>.",
        "severity": 0
    },
    "SENTENCE_STARTS_WITH_FORMULA": {
        "msg": "Typically a sentence should not start with a formula. You can pretty much always add some introductory words. For instance, instead of <code>$G$ is connected.</code> write <code>Graph $G$ is connected.</code>",
        "severity": 0
    },
    "SENTENCE_STARTS_WITH_NUMBER": {
        "msg": "Typically a sentence should not start with a number. Consider using numerals or reordering the sentenced. <code>5 persons can form a queue in $5!$ ways.</code> you could write <code>Five persons\u2026</code> or <code>Note that 5 persons\u2026</code>",
        "severity": 5
    },
    "RUSSIAN_TYPOGRAPHY_PECULIARITIES": {
        "msg": "Strictly speaking, this is not an error, but in the Russian typographic tradition, it is customary to denote the empty set with the symbol <code>\\varnothing</code>, not <code>\\emptyset</code> (the latter is more flattened). Similarly, instead of <code>\\epsilon</code> it is better to write <code>\\varepsilon</code>, and instead of <code>\\phi</code> write <code>\\varphi</code>.",
        "severity": 0
    },
    "BETTER_TO_USE_WORDS_THEN_MATH": {
        "msg": "Constructs like <code>the number of elements $=m^2$</code> are unacceptable in proper mathematical writing except for taking short personal notes. Symbols  \\(=, \\gt, \\geqslant\\) and such should be replaced with words if surrounded by words: <code>\u2026does not exceed $m^2$</code>, <code>\u2026equals $m^2$</code> etc.",
        "severity": 0
    },
    "MATH_ENVIRONMENT_VERBOSITY_WARNING": {
        "msg": "The <code>math</code> environment is not popular in \\(\\LaTeX\\) community. You can use a shorter (and absolutely equivalent in terms of what you get of it) construct <code>\\(\u2026\\)</code> or <code>$\u2026$</code>. Note also that <em>math</em> does not make a display-style formula, it opens the standard inline-math mode. For display math use <code>\\[\u2026\\]</code> or one of the environments <em>equation</em>, <em>array</em> etc.",
        "severity": 0
    },
    "USE_DIVIDES_INSTEAD_OF_VDOTS": {
        "msg": "Command <code>\\vdots</code> should be primarily used for typesetting matrices as a vertical ellipsis. When writing on divisibility of numbers, consider using vertical line (\u201c\u2026devides\u2026\u201d) instead of triple vertical dots (\u201c\u2026is divisible by\u2026\u201d).",
        "severity": 0
    },
    "MAKE_LONG_FORMULA_DISPLAY": {
        "msg": "Long formulas that take a lot of screen space should generally be thoughtfully typeset with proper AMS environments: see the list of these environments and their usecases <a href=\"https://www.overleaf.com/learn/latex/Aligning_equations_with_amsmath\" target=\"_blank\">here</a>.",
        "severity": 0
    },
    "EN_ORDINAL_ABBREVIATION": {
        "msg": "Possibly wrong ordinal abbreviation, see <a href=\"https://www.grammarly.com/blog/how-to-write-ordinal-numbers-correctly/\" target=\"_blank\">details</a>.",
        "severity": 0
    },
    "LATE_DEFINITION": {
        "msg": "Instead of writing <q><code>$x=a+b$</code>, where <code>$a=\u2026</code></q> it's better to introduce all the letters first and then write the expression containing these letters. See <a href=\"https://1drv.ms/w/s!AiAwrmxQ9QLrjOtTQqAXWdl3ryK5Jg?e=vEMU6W\" target=\"_blank\">P. Halmos's article</a>, the section 'Use Words Correctly'.",
        "severity": 0
    },
    "INVISIBLE_BRACES": {
        "msg": "To typeset braces you should write <code>\\{\u2026\\}</code>. Without backslashes the braces <code>{\u2026}</code> are the semantic delimiters in code, but are not displayed in the PDF.",
        "severity": 0
    },
    "MANUAL_LISTS": {
        "msg": "Avoid manual numbering in lists. Employ <em>enumerate</em> environment: <code>\\begin{enumerate}\\item Firstly\u2026 \\item Secondly\u2026 \\end{enumerate}</code>. Learn more about typesetting lists <a href=\"https://www.overleaf.com/learn/latex/Lists\" target=\"_blank\">here</a>.",
        "severity": 0
    },
    "MISMATCHED_MATH_DELIMITERS": {
        "msg": "Possibly mismatched math delimiters.",
        "severity": 0
    },
    "EN_ORDINAL_ABBREVIATION_IN_MATH": {
        "msg": "Ordinal abbreviations are textual, not mathematical pieces. See <a href=\"https://tex.stackexchange.com/a/4119\" target=\"_blank\">details</a> on how to properly typeset them in \\(\\LaTeX\\) if you\u2019d like to keep the superscript style.",
        "severity": 0
    },
    "LATIN_LETTER_OUTSIDE_MATH_EN": {
        "msg": "Even a single letter (if this letter has a mathematical semantics) should be typeset in math mode.",
        "severity": 0
    }
}