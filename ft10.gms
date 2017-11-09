$ontext

    Job Shop Scheduling

    Manne formulation

    Alan Manne, "On the job-shop scheduling problem", Operations Research
    vol 8, no 2 March-April 1960.

 job1:   0 29 ; 1 78 ; 2  9 ; 3 36 ; 4 49 ; 5 11 ; 6 62 ; 7 56 ; 8 44 ; 9 21
 job2:   0 43 ; 2 90 ; 4 75 ; 9 11 ; 3 69 ; 1 28 ; 6 46 ; 5 46 ; 7 72 ; 8 30
 job3:   1 91 ; 0 85 ; 3 39 ; 2 74 ; 8 90 ; 5 10 ; 7 12 ; 6 89 ; 9 45 ; 4 33
 job4:   1 81 ; 2 95 ; 0 71 ; 4 99 ; 6  9 ; 8 52 ; 7 85 ; 3 98 ; 9 22 ; 5 43
 job5:   2 14 ; 0  6 ; 1 22 ; 5 61 ; 3 26 ; 4 69 ; 8 21 ; 7 49 ; 9 72 ; 6 53
 job6:   2 84 ; 1  2 ; 5 52 ; 3 95 ; 8 48 ; 9 72 ; 0 47 ; 6 65 ; 4  6 ; 7 25
 job7:   1 46 ; 0 37 ; 3 61 ; 2 13 ; 6 32 ; 5 21 ; 9 32 ; 8 89 ; 7 30 ; 4 55
 job8:   2 31 ; 0 86 ; 1 46 ; 5 74 ; 4 32 ; 6 88 ; 8 19 ; 9 48 ; 7 36 ; 3 79
 job9:   0 76 ; 1 69 ; 3 76 ; 5 51 ; 2 85 ; 9 11 ; 6 40 ; 7 89 ; 4 26 ; 8 74
 job10:  1 85 ; 0 13 ; 2 61 ; 6  7 ; 8 64 ; 9 76 ; 5 47 ; 3 52 ; 4 90 ; 7 45


  Description: jobs need to follow a sequence of operations. The numbers indicate
  machine number and processing time.

  This is a well-known benchmark problem and the optimal obj=930.

$offtext

set
  j 'tasks' / job1*job10/
  m 'machines' /mach0*mach9/
  t 'stages'  /t1*t10/
;

alias(m,m2);

table proctimet(j,t) 'processing times'
        t1    t2    t3    t4    t5    t6    t7    t8    t9   t10
job1    29    78     9    36    49    11    62    56    44   21
job2    43    90    75    11    69    28    46    46    72   30
job3    91    85    39    74    90    10    12    89    45   33
job4    81    95    71    99     9    52    85    98    22   43
job5    14     6    22    61    26    69    21    49    72   53
job6    84     2    52    95    48    72    47    65     6   25
job7    46    37    61    13    32    21    32    89    30   55
job8    31    86    46    74    32    88    19    48    36   79
job9    76    69    76    51    85    11    40    89    26   74
job10   85    13    61     7    64    76    47    52    90   45
;

table prec(j,t) 'precedence relations: machine numbers'
        t1  t2  t3  t4  t5  t6  t7  t8  t9  t10
job1    0    1   2   3   4   5   6   7   8   9
job2    0    2   4   9   3   1   6   5   7   8
job3    1    0   3   2   8   5   7   6   9   4
job4    1    2   0   4   6   8   7   3   9   5
job5    2    0   1   5   3   4   8   7   9   6
job6    2    1   5   3   8   9   0   6   4   7
job7    1    0   3   2   6   5   9   8   7   4
job8    2    0   1   5   4   6   8   9   7   3
job9    0    1   3   5   2   9   6   7   4   8
job10   1    0   2   6   8   9   5   3   4   7
;

parameter mval(m) 'machine numbers';
mval(m) = ord(m)-1;

set sprec(j,m,m2) 'set version of parameter prec';
loop(t$(ord(t)>1),
   sprec(j,m,m2)$(mval(m)=prec(j,t-1) and mval(m2)=prec(j,t)) = yes;
);
option sprec:0:0:1;
display sprec;

parameter proctime(j,m);
proctime(j,m) = sum(t$(mval(m)=prec(j,t)),proctimet(j,t));

alias (j,k);

variables
  x(j,m)    'start time of task'
  y(j,k,m)  'binary variable to implement non-overlap: j after k'
  z         'objective variable'
;
binary variable y;
positive variable x;


scalar TMAX 'max time horizon';
TMAX = sum((j,m),proctime(j,m));

equations
   NoOverlap1(j,k,m)   'machine occupation'
   NoOverlap2(j,k,m)   'machine occupation'
   Precedence(j,m,m2)  'orders need to follow a certain sequence of machines'
   zmax(j,m)           'make span'
;

set jk(j,k);
jk(j,k)$(ord(j)<ord(k))=yes;

Precedence(sprec(j,m,m2)).. x(j,m2) =G= x(j,m) + proctime(j,m);

NoOverlap1(jk(j,k),m).. x(j,m) =G= x(k,m) + proctime(k,m) - TMAX*y(j,k,m);
NoOverlap2(jk(j,k),m).. x(k,m) =G= x(j,m) + proctime(j,m) - TMAX*(1-y(j,k,m));

zmax(j,m).. z =G= x(j,m) + proctime(j,m);

option optcr=0;
model jobshop /all/;
solve jobshop minimizing z using mip;