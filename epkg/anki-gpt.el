;;; gpt-anki.el  -*- lexical-binding: t; -*-

;; Copyright (C) 2024 The Ink Pot Monkey

;; Author: The Ink Pot Monkey <inkpotmonkey@palebluebytes.space>
;; URL: https://github.com/ink-pot-monkey/gpt-anki/epkgs/gpt-anki.el
;; Version: 0.1-pre
;; Package-Requires: ((emacs "29.2"))
;; Keywords: gpt anki

;; This file is not part of GNU Emacs.

;; This program is free software; you can redistribute it and/or modify
;; it under the terms of the GNU General Public License as published by
;; the Free Software Foundation, either version 3 of the License, or
;; (at your option) any later version.

;; This program is distributed in the hope that it will be useful,
;; but WITHOUT ANY WARRANTY; without even the implied warranty of
;; MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
;; GNU General Public License for more details.

;; You should have received a copy of the GNU General Public License
;; along with this program.  If not, see <http://www.gnu.org/licenses/>.

;;; Commentary:

;; This package allows easy usage of the gpt anki deck generator distributed with this flake

;;;; Installation

;;;;; Nix

;; Add this flake to your inputs: gpt-anki.url = "github:ink-pot-monkey/gpt-anki?ref=commandline";
;; Install this package emacs packages configuration, the command line tool will be automatically added

;;;; Usage

;; Run one of these commands:

;; `gpt-anki-generate-flashcards': Create a anki deck with the selected text or file

;;;; Tips

;; + You can customize settings in the `gpt-anki' group.

;;;; Credits

;; This package would not have been possible without the following
;; packages: foo[1], which showed me how to bifurcate, and bar[2],
;; which takes care of flanges.
;;
;;  [1] https://example.com/foo.el
;;  [2] https://example.com/bar.el

;;; Code:

;;;; Requirements

(require 'foo)
(require 'bar)

;;;; Customization

(defgroup gpt-anki nil
  "Settings for `gpt-anki'."
  :link '(url-link "https://example.com/gpt-anki.el"))

(defcustom gpt-anki-api-key nil
  "An API key (string) for OpenAI.

Can also be a function of no arguments that returns an API
key (more secure) for the active backend."
  :group 'gpt-anki
  :type '(choice
          (string :tag "API key")
          (function :tag "Function that returns the API key")))

;;;; Variables

(defvar gpt-anki-var nil
  "A variable.")

;;;;; Keymaps

;; This technique makes it easier and less verbose to define keymaps
;; that have many bindings.

(defvar gpt-anki-map
  ;; This makes it easy and much less verbose to define keys
  (let ((map (make-sparse-keymap "gpt-anki map"))
        (maps (list
               ;; Mappings go here, e.g.:
               "RET" #'gpt-anki-RET-command
               [remap search-forward] #'gpt-anki-search-forward
               )))
    (cl-loop for (key fn) on maps by #'cddr
             do (progn
                  (when (stringp key)
                    (setq key (kbd key)))
                  (define-key map key fn)))
    map))

;;;; Commands

;;;###autoload
(defun gpt-anki-generate-flashcards (deckname)
  "Generate a Anki deck with the name `DECKNAME'.
   
When in Dired the input will default to the file under the cursor.
   
If a region is selected in a buffer this becomes the input otherwise the whole buffer is sent as the input from which to create the flash cards."
  (interactive (list (read-string "Deck name: ")))
  (let* ((program "generate-flashcards")
         (dired-file (when (eq major-mode 'dired-mode)
                       (dired-get-file-for-visit)))
         (start (if (use-region-p) (region-beginning) (point-min)))
         (end (if (use-region-p) (region-end) (point-max)))
         (region-input (buffer-substring-no-properties start end)))
    (call-process program nil nil nil deckname gpt-anki-api-key (or dired-file region-input))))

;;;; Functions

;;;;; Public

(defun gpt-anki-foo (args)
  "Return foo for ARGS."
  (foo args))

;;;;; Private

(defun gpt-anki--bar (args)
  "Return bar for ARGS."
  (bar args))

;;;; Footer

(provide 'gpt-anki)

;;; gpt-anki.el ends here
