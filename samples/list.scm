(define pair (lambda (a b) (lambda (f) (f a b))))
(define first (lambda (t) (t (lambda (x y) x))))
(define second (lambda (t) (t (lambda (x y) y))))

(define p (pair 10 20))

(define empty (pair 0 0))
(define append (lambda (v l) (pair v l)))

(define len (lambda (l) 
                (if
                    (= (second l) 0) 0  ( + 1 (len (second l))))))


(define nth (lambda (l n) 
                (if (= n 0) (first l) (nth (second l) (- n 1)))))



(define l (append 10 (append 20 empty)))
(define m (append 30 l))

(define answer (let ((n 3))
(nth m (- (len m) n))))

(if (= answer 30) 100 0)


