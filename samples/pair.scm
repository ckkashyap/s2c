(define pair (lambda (a b) (lambda (f) (f a b))))
(define first (lambda (t) (t (lambda (x y) x))))
(define second (lambda (t) (t (lambda (x y) y))))

(define p (pair 10 20))

(if (and (= 10 (first p)) (= 20 (second p))) 100 0)
