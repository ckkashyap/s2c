(define data (get-input-buffer))
(define width (peek32 data 0))
(define height (peek32 data 1))
(define buffer (peekptr data 1))

(define debug-buffer (new-buffer 10))

(poke64 debug-buffer 0 (* 3 (* 800 800)))
(print-buffer debug-buffer 10)



(define setzeroall
  (lambda (n)
    (if (= n  0)
        (poke8 buffer n 0)
      (let ((x 0))
        (poke8 buffer n 0)
        (setzeroall (- n 1))))))


(setzeroall (- (* 4 (* width height)) 1))

1
