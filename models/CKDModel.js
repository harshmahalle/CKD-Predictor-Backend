const mongoose = require('mongoose');

const CKDSchema = new mongoose.Schema({
  sg: { type: Number, required: true },
  al: { type: Number, required: true },
  sc: { type: Number, required: true },
  hemo: { type: Number, required: true },
  pcv: { type: Number, required: true },
  htn: { type: Number, required: true }, 
  classification: { type: String }, 
}, { timestamps: true });

module.exports = mongoose.model('CKD', CKDSchema);
