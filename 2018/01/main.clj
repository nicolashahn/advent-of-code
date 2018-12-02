; Part 1
(with-open [rdr (clojure.java.io/reader "in.txt")]
  (println (reduce + (map read-string (line-seq rdr)))))

; Part 2
(with-open [rdr (clojure.java.io/reader "in.txt")]
  (let [nums (map read-string (line-seq rdr))]
    (def curr 0)
    (def ret nil)
    (def seen #{})
    (while (nil? ret)
      (doseq [n nums]
        (def curr (+ n curr))
        (if (and (contains? seen curr) (nil? ret))
          ; how does one break out of a doseq?
          (def ret curr)
          (def seen (conj seen curr)))))
    (println ret)))
