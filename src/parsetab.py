
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.2'

_lr_method = 'LALR'

_lr_signature = "T1\xdf\xd4C\x00\xc8Y\x8d\x0fn'qd\x80I"
    
_lr_action_items = {')':([6,7,9,],[8,-4,-3,]),'TYPE':([2,],[4,]),'(':([4,],[5,]),'[':([0,8,11,],[2,2,2,]),'PROPERTY':([5,7,],[7,7,]),']':([3,8,10,11,12,],[-2,-5,11,-5,-1,]),'$end':([0,1,3,11,12,],[-5,0,-2,-5,-1,]),}

_lr_action = { }
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = { }
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'expression':([0,8,11,],[1,10,12,]),'empty':([0,8,11,],[3,3,3,]),'property_list':([5,7,],[6,9,]),}

_lr_goto = { }
for _k, _v in _lr_goto_items.items():
   for _x,_y in zip(_v[0],_v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = { }
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> expression","S'",1,None,None,None),
  ('expression -> [ TYPE ( property_list ) expression ] expression','expression',8,'p_expression','/Users/Fluffy/ie/git/src/parseflow.py',47),
  ('expression -> empty','expression',1,'p_expression','/Users/Fluffy/ie/git/src/parseflow.py',48),
  ('property_list -> PROPERTY property_list','property_list',2,'p_property_list','/Users/Fluffy/ie/git/src/parseflow.py',61),
  ('property_list -> PROPERTY','property_list',1,'p_property_list','/Users/Fluffy/ie/git/src/parseflow.py',62),
  ('empty -> <empty>','empty',0,'p_empty','/Users/Fluffy/ie/git/src/parseflow.py',69),
]
