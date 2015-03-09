---
brief: DRM transmitter using GNU Radio
contact:
  author: KIT CEL
  email: uncnr[at]student.kit.edu
copyright_owner:
- Felix Wunsch
- Communications Engineering Lab, Karlsruhe Institute of Technology
dependencies:
- UHD
- FAAC
- FAAD2
gr_compatability:
  max: v3.7.*
  min: v3.7
repo: https://github.com/kit-cel/gr-drm.git
stable_release: master
title: gr-drm
type: application
website: https://github.com/kit-cel/gr-drm
readmeraw: https://raw.githubusercontent.com/kit-cel/gr-drm/master/README.md
--- 

This project features a DRM/DRM+ software transmitter fully integrated into GNU
Radio Companion.

You are also free to play around with several robustness modes (RM) and
spectrum occupancies (SO, signal bandwidth) ranging from 4.5 to 20 kHz. The
corresponding bit rates vary from below 5 kbps to about 55 kbps. A
configuration that is widely used is RM B (==1) and 10 kHz bandwidth (SO 3).
Among other parameters, the station label and a text message can also be set by
simply adapting the correspondant blocks' values.
