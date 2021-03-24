#!/bin/bash
echo "
const Yitizi = {
  yitiziData: `cat yitizi.json`,
  get:
  /**
   * Get all the variant characters of a given character.
   * @param {string} c A Chinese character.
   * @returns {string[]} All the variant characters of the given character.
   */
  function get(c) {
    const res = this.yitiziData[c];
    return res == null ? [] : [...res];
  }
};
try { module.exports = exports = Yitizi; } catch (e) {}" > javascript/index.js
