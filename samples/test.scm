(define do-times
  (lambda (iter fun)
    (if (= iter 1) (fun 0) (let () (fun (- iter 1)) (do-times (- iter 1) fun)))))

(define foreach-pixel
  (lambda (height width fcnt)
    (do-times height
              (lambda (row)
                (do-times width
                          (lambda (col) (fcnt col row)))))))

(foreach-pixel  4 4 (lambda (rr cc) (display rr)))
