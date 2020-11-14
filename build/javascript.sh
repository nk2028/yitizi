#!/bin/bash
echo "
const Yitizi = {
    yitiziData: `cat yitizi.json`,
    get: function get(c) {
    const res = this.yitiziData[c];
    return res == null ? [] : [...res];
    }
};
try { module.exports = exports = Yitizi; } catch (e) {}
" > javascript/index.js
