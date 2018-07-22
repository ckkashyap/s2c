(define true (and))
(define false (or))

(define x1 (if (and) 1 0))
(define x2 (+ x1 (if (and (= 1 1)) 1 0)))
(define x3 (+ x2 (if (and false false) 0 1)))
(define x4 (+ x3 (if (and false true) 0 1)))
(define x5 (+ x4 (if (and true false) 0 1)))
(define x6 (+ x5 (if (and true true) 1 0)))

(define x7 (+ x6 (if (or) 0 1)))
(define x8 (+ x7 (if (or (= 1 1)) 1 0)))
(define x9 (+ x8 (if (or false false) 0 1)))
(define x10 (+ x9 (if (or false true) 1 0)))
(define x11 (+ x10 (if (or true false) 1 0)))
(define x12 (+ x11 (if (or true true) 1 0)))


(if (= x12 12) 100)

