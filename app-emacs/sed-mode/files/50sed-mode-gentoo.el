;;; sed-mode site-lisp configuration

(add-to-list 'load-path "/usr/share/emacs/site-lisp/sed-mode")
(autoload 'sed-mode "sed-mode"
  "Major mode for editing sed scripts" t)
(add-to-list 'auto-mode-alist '("\\.sed\\'" . sed-mode))
(add-to-list 'interpreter-mode-alist '("sed" . sed-mode))
