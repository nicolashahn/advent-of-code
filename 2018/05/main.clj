(def polymer (with-open [rdr (clojure.java.io/reader "in.txt")]
              (first (line-seq rdr))))

(def alphabet "abcdefghijklmnopqrstuvwxyz")
(def lus (map str (seq alphabet) (seq (clojure.string/upper-case alphabet))))
(def uls (map str (seq (clojure.string/upper-case alphabet)) (seq alphabet)))
(def all-pairs (concat lus uls))

; remove all instances of the pair in the polymer
(defn react-pair [poly pair]
  (clojure.string/replace poly pair ""))

; remove all instances of all pairs from the polymer
(defn react-pairs [poly]
  (reduce #(react-pair %1 %2) poly all-pairs))

; do react-pairs continually until there are no more pairs to remove
(defn react-completely [poly]
  (def poly-atom (atom poly))
  (while (< (count (react-pairs @poly-atom)) (count @poly-atom))
    (swap! poly-atom react-pairs))
  @poly-atom)

; Part 1
(println (count (react-completely polymer)))
