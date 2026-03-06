import React, { useState, useEffect } from 'react';
import { Upload as UploadIcon, FileText, Loader2, Download } from 'lucide-react';
import { projectsAPI, activitiesAPI } from '../api';

const Upload = () => {
  const [projects, setProjects] = useState([]);
  const [selectedProject, setSelectedProject] = useState('');
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState(null);
  const [manualMode, setManualMode] = useState(false);
  const [formData, setFormData] = useState({ developer_name: '', module_name: '', commit_count: 0, lines_added: 0, lines_deleted: 0, files_modified: 0, bug_count: 0 });
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    fetchProjects();
  }, []);

  const fetchProjects = async () => {
    try {
      const res = await projectsAPI.getAll();
      setProjects(res.data);
      if (res.data.length > 0) setSelectedProject(res.data[0].id);
    } catch (err) {
      console.error('Failed to fetch projects:', err);
    }
  };

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      if (!selectedFile.name.endsWith('.csv')) {
        setMessage({ type: 'error', text: 'Please select a CSV file' });
        return;
      }
      setFile(selectedFile);
      setMessage(null);
    }
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!selectedProject || !file) {
      setMessage({ type: 'error', text: 'Please select a project and file' });
      return;
    }
    setUploading(true);
    setMessage(null);
    try {
      const res = await activitiesAPI.upload(selectedProject, file);
      setMessage({ type: 'success', text: `Successfully uploaded ${res.data.records_added} activities` });
      setFile(null);
    } catch (err) {
      setMessage({ type: 'error', text: err.response?.data?.detail || 'Upload failed' });
    } finally {
      setUploading(false);
    }
  };

  const handleManualSubmit = async (e) => {
    e.preventDefault();
    if (!selectedProject) {
      setMessage({ type: 'error', text: 'Please select a project' });
      return;
    }
    setSubmitting(true);
    setMessage(null);
    try {
      await activitiesAPI.create({ project_id: selectedProject, ...formData });
      setMessage({ type: 'success', text: 'Activity added successfully' });
      setFormData({ developer_name: '', module_name: '', commit_count: 0, lines_added: 0, lines_deleted: 0, files_modified: 0, bug_count: 0 });
    } catch (err) {
      setMessage({ type: 'error', text: err.response?.data?.detail || 'Failed to add activity' });
    } finally {
      setSubmitting(false);
    }
  };

  const downloadSample = () => {
    const csv = 'developer_name,module_name,commit_count,lines_added,lines_deleted,files_modified,bug_count\njohndoe,Authentication,15,500,200,8,2\njanesmith,PaymentService,22,800,300,12,5\nbobwilson,UserManagement,10,300,100,5,1';
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'sample_activity.csv';
    a.click();
  };

  return (
    <div className="space-y-6 animate-fadeIn">
      <div>
        <h1 className="text-2xl font-bold text-white">Data Upload</h1>
        <p className="text-slate-400">Upload development activity data</p>
      </div>

      <div className="flex gap-2 mb-4">
        <button onClick={() => setManualMode(false)} className={`btn ${!manualMode ? 'btn-primary' : 'btn-secondary'}`}>CSV Upload</button>
        <button onClick={() => setManualMode(true)} className={`btn ${manualMode ? 'btn-primary' : 'btn-secondary'}`}>Manual Entry</button>
      </div>

      <div className="card">
        <div className="mb-4">
          <label className="block text-sm font-medium text-slate-300 mb-2">Select Project</label>
          <select value={selectedProject} onChange={(e) => setSelectedProject(e.target.value)} className="input">
            {projects.map((p) => (<option key={p.id} value={p.id}>{p.name}</option>))}
          </select>
        </div>

        {!manualMode ? (
          <form onSubmit={handleUpload} className="space-y-4">
            <div className="border-2 border-dashed border-dark-600 rounded-lg p-8 text-center">
              <UploadIcon className="w-12 h-12 text-slate-500 mx-auto mb-4" />
              <p className="text-slate-400 mb-4">{file ? file.name : 'Drop your CSV file here or click to browse'}</p>
              <input type="file" accept=".csv" onChange={handleFileChange} className="hidden" id="file-input" />
              <label htmlFor="file-input" className="btn btn-secondary cursor-pointer inline-block">Choose File</label>
            </div>
            <div className="flex gap-3">
              <button type="button" onClick={downloadSample} className="btn btn-secondary"><Download className="w-4 h-4" /> Sample CSV</button>
              <button type="submit" disabled={uploading || !file} className="btn btn-primary flex-1">
                {uploading ? <Loader2 className="w-4 h-4 animate-spin" /> : <><UploadIcon className="w-4 h-4" /> Upload</>}
              </button>
            </div>
          </form>
        ) : (
          <form onSubmit={handleManualSubmit} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">Developer Name</label>
                <input type="text" value={formData.developer_name} onChange={(e) => setFormData({ ...formData, developer_name: e.target.value })} className="input" required />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">Module Name</label>
                <input type="text" value={formData.module_name} onChange={(e) => setFormData({ ...formData, module_name: e.target.value })} className="input" required />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">Commit Count</label>
                <input type="number" value={formData.commit_count} onChange={(e) => setFormData({ ...formData, commit_count: parseInt(e.target.value) || 0 })} className="input" min="0" />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">Lines Added</label>
                <input type="number" value={formData.lines_added} onChange={(e) => setFormData({ ...formData, lines_added: parseInt(e.target.value) || 0 })} className="input" min="0" />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">Lines Deleted</label>
                <input type="number" value={formData.lines_deleted} onChange={(e) => setFormData({ ...formData, lines_deleted: parseInt(e.target.value) || 0 })} className="input" min="0" />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">Files Modified</label>
                <input type="number" value={formData.files_modified} onChange={(e) => setFormData({ ...formData, files_modified: parseInt(e.target.value) || 0 })} className="input" min="0" />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">Bug Count</label>
                <input type="number" value={formData.bug_count} onChange={(e) => setFormData({ ...formData, bug_count: parseInt(e.target.value) || 0 })} className="input" min="0" />
              </div>
            </div>
            <button type="submit" disabled={submitting} className="btn btn-primary w-full">
              {submitting ? <Loader2 className="w-4 h-4 animate-spin" /> : 'Add Activity'}
            </button>
          </form>
        )}
      </div>

      {message && (
        <div className={`p-4 rounded-lg ${message.type === 'success' ? 'bg-success/20 text-success border border-success/50' : 'bg-danger/20 text-danger border border-danger/50'}`}>
          {message.text}
        </div>
      )}
    </div>
  );
};

export default Upload;
