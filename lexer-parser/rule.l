<PROGRAMME>    ::= <PROGRAMME><Declarations> | <PROGRAMME><VariableDeclaration> | <EPSILON>;

<Declarations> ::=
    <T_INT> <T_IDENTIFIER> <T_(> <ArgumentDeclaration> <T_)> <Block> |
    <T_VOID> <T_IDENTIFIER> <T_(> <ArgumentDeclaration> <T_)> <Block>;

<ArgumentDeclaration> ::= <Argument_,>* <T_INT><T_IDENTIFIER> | <T_INT><T_IDENTIFIER>|<T_VOID>  | <EPSILON>;
<Argument_,> ::= <T_INT><T_IDENTIFIER> <T_,>;

<Block> ::= <T_{> <Sentences> <T_}>|<Sentence>;

<Sentences> ::= <Sentence><Sentence>*;
<Sentence> ::= <IfSentence> | <WhileSentence> | <ReturnSentence> | <VariableDeclaration> | <AssignSentence>;

<VariableDeclaration> ::=
    <T_INT><T_IDENTIFIER><T_=><Expression><T_;> |
    <T_INT><T_IDENTIFIER><T_;>;

<AssignSentence> ::= <T_IDENTIFIER><T_=><Expression><T_;>;
 
<ReturnSentence> ::= <T_RETURN><Expression><T_;> | <T_RETURN><T_;>;
<WhileSentence> ::= <T_WHILE><T_(><Expression><T_)><Block>;

<IfSentence> ::= <T_IF><T_(><Expression><T_)><Block><T_ELSE><Block> | <T_IF><T_(><Expression><T_)><Block>;
// <Expression> ::= <Expression><Relop><Item> | <Item>; 
// <Item> ::= <T_(><Expression><T_)> | <T_INTEGER> | <CallFunction> | <T_IDENTIFIER>;
<CallFunction> ::= <T_IDENTIFIER><T_(><ArgumentList><T_)>;
<ArgumentList> ::= <ArgumentList><T_,><Expression> | <Expression><EPSILON>;
// <Relop> ::= <T_==> | <T_>=> | <T_<=> | <T_!=> | <T_>> | <T_<> | <T_+> | <T_-> | <T_*> | <T_/>;
<Expression> ::= <AddExpression><XAddExpression>*;
<XAddExpression> ::= <Relop><AddExpression>;
<Relop> ::= <T_==> | <T_>=> | <T_<=> | <T_!=> | <T_>> | <T_<>;
<AddExpression> ::= <Item><XItem>*;
<XItem> ::= <T_+><Item> | <T_-><Item>;
<Item> ::= <Factor><XFactor>*;
<XFactor> ::= <T_*><Factor> | <T_/><Factor>;
<Factor> ::= <T_INTEGER> | <T_(><Expression><T_)> |
             <T_IDENTIFIER><FTYPE>;
<FTYPE> ::= <CallFunction> | <EPSILON>;
