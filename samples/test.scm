
(define do-times
  (lambda (i f)
    (if (= i 1) (f 0) (let () (f (- i 1)) (do-times (- i 1) f)))))

(define foreach-pixel
  (lambda (h w f)
    (do-times h
              (lambda (r)
                (do-times w
                          (lambda (c) (f c r)))))))


(foreach-pixel  4 4 (lambda (r c) (display r)))

100
