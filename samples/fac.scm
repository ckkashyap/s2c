(define fac (lambda (n)
  (if (= n 0) 1 (* n (fac (- n 1))))))

(if (= 120 (fac 5)) 100 0)
