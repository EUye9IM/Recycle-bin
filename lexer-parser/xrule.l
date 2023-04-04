<PROGRAMME> ::= <Declarations>;
<Declarations> ::= <Declaration><Declaration>*;
<Declaration> ::= <T_INT><T_IDENTIFIER><DeclarationType> |
                  <T_VOID><T_IDENTIFIER><FunDeclaration>;
<DeclarationType> ::= <VarDeclaration> | <FunDeclaration>;
<VarDeclaration> ::= <T_;>;
<FunDeclaration> ::= <T_(><FormalParam><T_)><Block>;
<FormalParam> ::= <ParamList> | <EPSILON> | <T_VOID>;
<ParamList> ::= <Param><XParam>*;
<XParam> ::= <T_,><Param>;
<Param> ::= <T_INT><T_IDENTIFIER>;
<Block> ::= <T_{><Sentences><T_}> | <T_{><T_}>;

<Sentences> ::= <Sentence><Sentence>*;
<Sentence> ::= <IfSentence> | <WhileSentence> | <ReturnSentence> | <AssignSentence> |
               <InnerDeclaration>;

<InnerDeclaration> ::= <InnerVarDeclare><InnerVarDeclare>*;
<InnerVarDeclare> ::= <T_INT><T_IDENTIFIER><T_;>;
<AssignSentence> ::= <T_IDENTIFIER><T_=><Expression><T_;>;
<ReturnSentence> ::= <T_RETURN><T_;> | <T_RETURN><Expression><T_;>;
<WhileSentence> ::= <T_WHILE><T_(><Expression><T_)><Block>;
<IfSentence> ::= <T_IF><T_(><Expression><T_)><Block> |
                 <T_IF><T_(><Expression><T_)><Block><T_ELSE><Block>;
<Expression> ::= <AddExpression><XAddExpression>*;
<XAddExpression> ::= <Relop><AddExpression>;
<Relop> ::= <T_==> | <T_>=> | <T_<=> | <T_!=> | <T_>> | <T_<>;
<AddExpression> ::= <Item><XItem>*;
<XItem> ::= <T_+><Item> | <T_-><Item>;
<Item> ::= <Factor><XFactor>*;
<XFactor> ::= <T_*><Factor> | <T_/><Factor>;
<Factor> ::= <T_INTEGER> | <T_(><Expression><T_)> |
             <T_IDENTIFIER><FTYPE>;
<FTYPE> ::= <CALL> | <EPSILON>;
<CALL> ::= <T_(><ActualParam><T_)>;
<ActualParam> ::= <ActualParamList> | <EPSILON>;
<ActualParamList> ::= <Expression><XExpression>*;
<XExpression> ::= <T_,><Expression>;


