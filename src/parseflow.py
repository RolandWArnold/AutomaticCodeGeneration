#!/usr/bin/env python

import sys, os, os.path
from ply import lex, yacc

from templates.template import LType
from templates.dialog import Dialog
from templates.filteredlist import FilteredList
from templates.basedialog import BaseDialog
from templates.basedialog_instance import BaseDialogInstance
from templates.wizard import Wizard, WizardPointer
from templates.component import Checkbox, Label, Combobox, ComboOption, Textbox, MenuItem, Picture, Whitespace, ItemList, HorizontalRule, Totals

components = {"Dialog" : Dialog, "BaseDialog" : BaseDialog, "BaseDialogInstance" : BaseDialogInstance, "MenuItem" : MenuItem,
    "FilteredList" : FilteredList, "Checkbox" : Checkbox, "Label" : Label, "Combobox" : Combobox, "Picture" : Picture,
    "ComboOption": ComboOption, "Textbox" : Textbox, "Whitespace" : Whitespace, "Wizard" : Wizard, "WizardPointer" : WizardPointer,
    "ItemList" : ItemList, "HorizontalRule" : HorizontalRule, "Totals" : Totals}

class LexFlow(object):
    def __init__(self):
        self.literals = "()[]"
        self.tokens = ('TYPE', 'PROPERTY')
        self.t_ignore  = ' \t'
        self.t_ignore_COMMENT = r'\#.*'
        self.t_TYPE = r'\bWizard\b|\bWizardPointer\b|\bFilteredList\b|\bBaseDialog\b|\bBaseDialogInstance\b|\bCheckbox\b|\bComboOption\b|\bCombobox\b|\bDialog\b|\bLabel\b|\bMenuItem\b|\bPicture\b|\bTextbox\b|\bWhitespace\b|\bItemList\b|\bHorizontalRule\b|\bTotals\b'
        self.lexer = lex.lex(object=self)
    
    def t_PROPERTY(self, t):
        r'\w*=\"[^"]*?\"\ ?'
        k, v = tuple(t.value.strip().split("=", 1))
        t.value = k, v.strip('"')
        return t
    
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)
    
    def t_error(self, t):
        print("Illegal character '%s' on line %s" % (t.value[0], t.lexer.lineno))
        t.lexer.skip(1)

class YaccFlow(object):
    def __init__(self, fname, root=None, silent=False):
        self.props = set()
        # Note: could split this up into the four possible expansions for expression
        def p_expression(p):
            """expression : '[' TYPE '(' property_list ')' expression ']' expression
                    | empty"""
            if p[1]:
                p[6] = p[6] or []
                index_dict = {}
                for child in p[6]:
                    tpl = (child.ctype, child.properties["name"],)
                    index_dict[tpl] = index_dict.get(tpl, -1) + 1
                    child.properties["index"] = index_dict[tpl]
                p[0] = [components[p[2]](root, p[2], p[4]["name"], p[6], p[4])]
                if p[8]:
                    p[0].extend(p[8])
        
        def p_property_list(p):
            """property_list : PROPERTY property_list
                            | PROPERTY"""
            key, value = p[1]
            self.props.add(key)
            p[0] = {} if len(p) == 2 else p[2]
            p[0][key] = value
        
        def p_empty(p):
            """empty :"""
        
        def p_error(p):
            print("Syntax error ('%s') in input at approx. line %s." % (p.value, p.lineno))
            self.success = False
        
        self.tree = []
        self.success = True
        tokens = LexFlow().tokens
        parser = yacc.yacc()
        if not silent:
            print("Parser: Using '%s'" % fname)
        with open(fname, "r") as f:
            self.tree = parser.parse(f.read())
            if not self.success:
                sys.exit(-2)
