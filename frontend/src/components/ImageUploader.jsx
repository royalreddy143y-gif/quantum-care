import React, { useState, useRef } from 'react';
import { UploadCloud, Image as ImageIcon, X, AlertCircle } from 'lucide-react';

export const ImageUploader = ({ onImageSelect, selectedImage, onClearImage, error }) => {
  const [isDragging, setIsDragging] = useState(false);
  const [previewUrl, setPreviewUrl] = useState(null);
  const fileInputRef = useRef(null);

  const handleFiles = (file) => {
    if (!file) return;

    // Validate type
    const validTypes = ['image/jpeg', 'image/jpg', 'image/png'];
    if (!validTypes.includes(file.type)) {
      alert("Please upload a valid medical image file (JPEG or PNG).");
      return;
    }

    // Validate size (10 MB)
    if (file.size > 10 * 1024 * 1024) {
      alert("File exceeds maximum allowable size of 10MB.");
      return;
    }

    const preview = URL.createObjectURL(file);
    setPreviewUrl(preview);
    onImageSelect(file, preview);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFiles(e.dataTransfer.files[0]);
    }
  };

  const handleClear = (e) => {
    e.stopPropagation();
    if (previewUrl) URL.revokeObjectURL(previewUrl);
    setPreviewUrl(null);
    if (fileInputRef.current) fileInputRef.current.value = '';
    onClearImage();
  };

  return (
    <div className="w-full space-y-2">
      <input
        ref={fileInputRef}
        type="file"
        accept=".jpg,.jpeg,.png"
        className="hidden"
        onChange={(e) => {
          if (e.target.files && e.target.files[0]) {
            handleFiles(e.target.files[0]);
          }
        }}
      />

      {previewUrl || selectedImage ? (
        <div className="relative rounded-2xl border-2 border-brand-500/30 bg-slate-50 p-4 overflow-hidden flex flex-col items-center">
          <button
            type="button"
            onClick={handleClear}
            className="absolute top-3 right-3 p-1.5 bg-slate-900/70 hover:bg-slate-900 text-white rounded-full transition-colors z-10"
            title="Remove image"
          >
            <X className="w-4 h-4" />
          </button>
          <div className="relative w-full max-h-72 flex justify-center items-center overflow-hidden rounded-xl bg-slate-900/5">
            <img
              src={previewUrl || selectedImage.preview}
              alt="Medical scan preview"
              className="max-h-72 max-w-full object-contain rounded-lg shadow-sm"
            />
          </div>
          <div className="mt-3 flex items-center justify-between w-full text-xs text-slate-500 px-2">
            <span className="font-medium text-slate-700 truncate max-w-xs">
              {selectedImage?.name || "Medical Scan"}
            </span>
            <span>
              {selectedImage ? `${(selectedImage.size / 1024).toFixed(1)} KB` : ''}
            </span>
          </div>
        </div>
      ) : (
        <div
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          onClick={() => fileInputRef.current?.click()}
          className={`flex flex-col items-center justify-center p-8 border-2 border-dashed rounded-2xl cursor-pointer transition-all duration-200 ${
            isDragging
              ? 'border-brand-500 bg-brand-50/50 scale-[1.01]'
              : 'border-slate-300 hover:border-brand-400 bg-slate-50/50 hover:bg-white'
          }`}
        >
          <div className="p-3 bg-brand-50 text-brand-600 rounded-full mb-3 shadow-sm">
            <UploadCloud className="w-7 h-7" />
          </div>
          <p className="text-sm font-semibold text-slate-800">
            Click to upload scan or drag and drop
          </p>
          <p className="text-xs text-slate-500 mt-1">
            Supported medical image formats: JPG, JPEG, PNG (Max 10MB)
          </p>
          <div className="mt-4 flex items-center gap-2 text-xs font-medium text-brand-600 bg-brand-50 px-3 py-1.5 rounded-lg border border-brand-100">
            <ImageIcon className="w-3.5 h-3.5" />
            <span>Ready for Swin Transformer Preprocessing</span>
          </div>
        </div>
      )}

      {error && (
        <div className="flex items-center gap-1.5 text-xs text-rose-600 font-medium">
          <AlertCircle className="w-4 h-4" />
          <span>{error}</span>
        </div>
      )}
    </div>
  );
};
