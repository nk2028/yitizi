#!/bin/bash
echo "
const Yitizi = {
  yitiziData: `cat yitizi.json`,
  /**
   * Get all the variant characters of a given character.
   * @param {string} c A Chinese character.
   * @returns {string[]} All the variant characters of the given character.
   */
  get(c) { return [...(this.yitiziData[c] || '')]; }
};
try { module.exports = exports = Yitizi; } catch (e) {}" > javascript/index.js
