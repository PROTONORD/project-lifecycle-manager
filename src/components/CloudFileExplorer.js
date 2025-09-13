import React, { useState, useEffect } from 'react';
import styles from './CloudFileExplorer.module.css';

const CloudFileExplorer = () => {
  const [cloudData, setCloudData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [selectedCloud, setSelectedCloud] = useState('jottacloud');

  useEffect(() => {
    // Last cloud-data fra JSON-filen
    fetch('/data/protonord_cloud_data.json')
      .then(response => response.json())
      .then(data => {
        setCloudData(data);
        setLoading(false);
      })
      .catch(error => {
        console.error('Feil ved lasting av cloud-data:', error);
        setLoading(false);
      });
  }, []);

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('no-NO', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  if (loading) {
    return (
      <div className={styles.loading}>
        <div className={styles.spinner}></div>
        <p>Laster cloud-filer...</p>
      </div>
    );
  }

  if (!cloudData) {
    return (
      <div className={styles.error}>
        <p>❌ Kunne ikke laste cloud-data</p>
      </div>
    );
  }

  const currentCloud = cloudData.clouds[selectedCloud];

  return (
    <div className={styles.cloudExplorer}>
      <div className={styles.header}>
        <h2>📁 ProtoNord Cloud Files</h2>
        <p className={styles.lastUpdated}>
          Sist oppdatert: {formatDate(cloudData.last_updated)}
        </p>
      </div>

      <div className={styles.cloudSelector}>
        <button
          className={`${styles.cloudButton} ${selectedCloud === 'jottacloud' ? styles.active : ''}`}
          onClick={() => setSelectedCloud('jottacloud')}
        >
          ☁️ Jottacloud ({cloudData.clouds.jottacloud.protonord_files.length} filer)
        </button>
        <button
          className={`${styles.cloudButton} ${selectedCloud === 'gdrive' ? styles.active : ''}`}
          onClick={() => setSelectedCloud('gdrive')}
        >
          📁 Google Drive ({cloudData.clouds.gdrive.protonord_files.length} filer)
        </button>
      </div>

      <div className={styles.content}>
        <div className={styles.treeStructure}>
          <h3>📂 Mappestruktur</h3>
          <pre className={styles.tree}>
            {currentCloud.tree_structure || 'Ingen mapper funnet'}
          </pre>
        </div>

        <div className={styles.fileList}>
          <h3>📄 Filer i {currentCloud.name}</h3>
          {currentCloud.protonord_files.length === 0 ? (
            <p className={styles.noFiles}>Ingen filer funnet i protonord-mappen</p>
          ) : (
            <div className={styles.files}>
              {currentCloud.protonord_files.map((file, index) => (
                <div key={index} className={styles.fileItem}>
                  <div className={styles.fileIcon}>
                    {file.IsDir ? '📁' : getFileIcon(file.Name)}
                  </div>
                  <div className={styles.fileDetails}>
                    <div className={styles.fileName}>{file.Name}</div>
                    <div className={styles.fileMeta}>
                      {!file.IsDir && (
                        <span className={styles.fileSize}>
                          {formatFileSize(file.Size)}
                        </span>
                      )}
                      <span className={styles.fileDate}>
                        {formatDate(file.ModTime)}
                      </span>
                    </div>
                    <div className={styles.filePath}>{file.Path}</div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

const getFileIcon = (fileName) => {
  const extension = fileName.split('.').pop()?.toLowerCase();
  
  const iconMap = {
    'pdf': '📄',
    'doc': '📝',
    'docx': '📝',
    'txt': '📄',
    'md': '📋',
    'jpg': '🖼️',
    'jpeg': '🖼️',
    'png': '🖼️',
    'gif': '🖼️',
    'mp4': '🎥',
    'mp3': '🎵',
    'zip': '📦',
    'rar': '📦',
    'xlsx': '📊',
    'xls': '📊',
    'pptx': '📊',
    'ppt': '📊'
  };
  
  return iconMap[extension] || '📄';
};

export default CloudFileExplorer;