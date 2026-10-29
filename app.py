# ===== NEW TAB 8 - DOCUMENTS FOR ALL 13 - PDF, POWERPOINT, WORD, EXCEL - FIXED =====
with tab8:
    st.subheader("📄 Upload Documents - PDF, PowerPoint, Word, Excel - For ALL 13 Departments!")
    st.info("✅ ALL 13 Departments can upload PDF, Excel, PowerPoint, Word - All see & download - Saved on server for years!")
    
    doc_cat=st.selectbox("Document Category", DOC_CATEGORIES, key="doc_cat")
    doc_title=st.text_input("Document Title * (e.g. Budget 2026, Constitution)", key="doc_title")
    doc_desc=st.text_area("Description / Details (Optional)", key="doc_desc", placeholder="Describe this document...")
    
    # ===== THIS ALLOWS PDF, PPT, WORD, EXCEL - ALL FORMATS =====
    doc_file=st.file_uploader(
        "Upload File * PDF / PowerPoint / Word / Excel - Any member of 13 can upload", 
        type=["pdf","xlsx","xls","pptx","ppt","docx","doc","csv","txt"], 
        key="doc_file",
        help="Supports: PDF (.pdf), PowerPoint (.pptx, .ppt), Word (.docx, .doc), Excel (.xlsx, .xls, .csv)"
    )
    
    if st.button("📤 Upload Document - Visible to ALL 13", type="primary", use_container_width=True, key="doc_save"):
        if not doc_title.strip() or not doc_file:
            st.error("❌ Title + File required! Upload PDF, PPT, Word, or Excel")
        else:
            did=len(st.session_state.uploaded_docs)+1
            # Save with original name
            safe_name = doc_file.name.replace(" ", "_")
            fpath=f"data/documents/doc_{did}_{safe_name}"
            open(fpath,'wb').write(doc_file.getvalue())
            
            # Detect file type icon
            ext = safe_name.split('.')[-1].lower()
            file_icon = "📄"
            if ext == "pdf": file_icon = "📕 PDF"
            elif ext in ["pptx","ppt"]: file_icon = "📊 PowerPoint"
            elif ext in ["docx","doc"]: file_icon = "📝 Word"
            elif ext in ["xlsx","xls","csv"]: file_icon = "📗 Excel"
            
            st.session_state.uploaded_docs.append({
                "id": did,
                "category": doc_cat,
                "title": doc_title.strip(),
                "description": doc_desc.strip(),
                "file_name": doc_file.name,
                "file_path": fpath,
                "file_type": doc_file.type,
                "file_ext": ext,
                "file_icon": file_icon,
                "size": doc_file.size,
                "by": user_full,
                "from": user,
                "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            })
            save_json(UPLOADED_DOCS_FILE, st.session_state.uploaded_docs)
            st.success(f"✅ Uploaded {file_icon} {doc_file.name}! ALL 13 departments can now see & download - Saved for years!"); 
            st.balloons()
            st.rerun()
    
    st.divider()
    # ===== VIEW AND DOWNLOAD FOR ALL 13 =====
    all_docs = load_json(UPLOADED_DOCS_FILE, st.session_state.uploaded_docs)
    st.subheader(f"📂 All Documents - {len(all_docs)} Files - PDF, PPT, Word, Excel - All 13 Can Download")
    
    # Filter
    col1, col2 = st.columns([1,2])
    with col1:
        docs_filter = st.selectbox("Filter by Category", ["All"]+DOC_CATEGORIES, key="docs_filter")
    with col2:
        type_filter = st.selectbox("Filter by File Type", ["All Types","📕 PDF","📊 PowerPoint","📝 Word","📗 Excel"], key="type_filter")
    
    filtered_docs = all_docs
    if docs_filter != "All":
        filtered_docs = [d for d in filtered_docs if d['category'] == docs_filter]
    if type_filter != "All Types":
        if "PDF" in type_filter: filtered_docs = [d for d in filtered_docs if d.get('file_ext','') == 'pdf']
        elif "PowerPoint" in type_filter: filtered_docs = [d for d in filtered_docs if d.get('file_ext','') in ['pptx','ppt']]
        elif "Word" in type_filter: filtered_docs = [d for d in filtered_docs if d.get('file_ext','') in ['docx','doc']]
        elif "Excel" in type_filter: filtered_docs = [d for d in filtered_docs if d.get('file_ext','') in ['xlsx','xls','csv']]
    
    if not filtered_docs:
        st.warning("No documents yet - Upload PDF, PowerPoint, Word, or Excel above! ALL 13 can upload!")
    else:
        for doc in reversed(filtered_docs):
            with st.container(border=True):
                st.markdown(f"{doc.get('file_icon','📄')} **{doc['title']}** | {doc['category']} | by {doc['by']} | {doc['date']}")
                if doc.get('description',''): 
                    st.write(f"📝 {doc['description']}")
                st.caption(f"File: {doc['file_name']} | Type: {doc.get('file_ext','').upper()} | Size: {doc.get('size',0)//1024} KB")
                
                if os.path.exists(doc.get('file_path','')):
                    try:
                        with open(doc['file_path'],'rb') as f:
                            file_data = f.read()
                        # Download button for ALL 13
                        st.download_button(
                            f"📥 Download {doc['file_name']}", 
                            file_data, 
                            file_name=doc['file_name'], 
                            mime=doc.get('file_type','application/octet-stream'), 
                            key=f"dl_doc_{doc['id']}_{doc['file_name']}", 
                            type="primary", 
                            use_container_width=True
                        )
                    except Exception as e:
                        st.error(f"File not found on server: {e}")
                else:
                    st.warning("⚠️ File missing on server - Re-upload needed")
