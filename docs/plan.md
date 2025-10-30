Of course. Here is the complete and explicit implementation plan designed for an AI coding agent. Each granular task includes the precise file to modify, the exact code block to find, and the exact code block to replace it with.

This plan is structured to be executed sequentially, minimizing risk and ensuring that changes do not create unintended side effects.

---

### **Implementation Plan for Discovery Page & Backend Refinements**

**Objective:** To implement a series of high-impact, low-risk improvements to the keyword discovery feature, focusing on backend intelligence, UI responsiveness, and architectural robustness, while adhering to the specified constraints.

---

### **Phase 1: High-Impact, Low-Risk Tasks**

#### **Task 1: Enhance Backend Discovery Logic**

**Goal:** Make the backend intelligently select the appropriate keyword discovery modes based on the number of keywords the user has requested, without changing the frontend UI.

*   **Granular Task 1.1: Modify the Discovery API Endpoint**
    *   **File:** `api/routers/discovery.py`
    *   **Action:** Find the `start_discovery_run_async` function and replace the hardcoded `discovery_modes` list with conditional logic based on the `limit` parameter.

    *   **Find this code block:**
        ```python
        @router.post("/clients/{client_id}/discovery-runs-async", response_model=JobResponse)
        async def start_discovery_run_async(
            client_id: str,
            request: DiscoveryRunRequest,
            orchestrator: WorkflowOrchestrator = Depends(get_orchestrator),
            discovery_service: DiscoveryService = Depends(get_discovery_service),
        ):
            if client_id != orchestrator.client_id:
                raise HTTPException(
                    status_code=403,
                    detail="You do not have permission to access this client's resources.",
                )
            try:
                filters = request.filters
                limit = request.limit or 1000
                discovery_modes = ["keyword_ideas", "keyword_suggestions", "related_keywords"]

                if limit <= 500:
                    depth = 2
                elif limit <= 2000:
                    depth = 3
                else:
                    depth = 4

                parameters = {
                    "seed_keywords": request.seed_keywords,
                    "discovery_modes": discovery_modes,
                    "filters": filters,
                    "order_by": request.order_by,
                    "filters_override": request.filters_override,
                    "limit": limit,
                    "depth": depth,
                    "include_clickstream_data": request.include_clickstream_data,  # NEW
                    "closely_variants": request.closely_variants,  # NEW
                    "ignore_synonyms": request.ignore_synonyms,  # NEW
                }
                run_id = discovery_service.create_discovery_run(
                    client_id=client_id, parameters=parameters
                )

                job_id = orchestrator.run_discovery_and_save(
                    run_id,
                    request.seed_keywords,
                    discovery_modes,
                    filters,
                    request.order_by,
                    request.filters_override,
                    limit,
                    depth,
                    request.ignore_synonyms,
                    request.include_clickstream_data,  # NEW
                    request.closely_variants,  # NEW
                )
                return {"job_id": job_id, "message": f"Discovery run job {job_id} started."}
            except Exception as e:
                logger.error(
                    f"Failed to start discovery run for client {client_id}: {e}", exc_info=True
                )
                raise HTTPException(
                    status_code=500, detail=f"Failed to start discovery run: {e}"
                )
        ```

    *   **Replace with this code block:**
        ```python
        @router.post("/clients/{client_id}/discovery-runs-async", response_model=JobResponse)
        async def start_discovery_run_async(
            client_id: str,
            request: DiscoveryRunRequest,
            orchestrator: WorkflowOrchestrator = Depends(get_orchestrator),
            discovery_service: DiscoveryService = Depends(get_discovery_service),
        ):
            if client_id != orchestrator.client_id:
                raise HTTPException(
                    status_code=403,
                    detail="You do not have permission to access this client's resources.",
                )
            try:
                filters = request.filters
                limit = request.limit or 1000
                
                # --- INTELLIGENT DISCOVERY MODE SELECTION ---
                if limit <= 500:
                    # For small, targeted requests, use precise modes.
                    discovery_modes = ["keyword_suggestions", "related_keywords"]
                    depth = 2
                elif limit <= 2000:
                    # For medium requests, use all modes.
                    discovery_modes = ["keyword_ideas", "keyword_suggestions", "related_keywords"]
                    depth = 3
                else:
                    # For large requests, prioritize broad discovery.
                    discovery_modes = ["keyword_ideas", "related_keywords"]
                    depth = 4
                # --- END OF CHANGE ---

                parameters = {
                    "seed_keywords": request.seed_keywords,
                    "discovery_modes": discovery_modes,
                    "filters": filters,
                    "order_by": request.order_by,
                    "filters_override": request.filters_override,
                    "limit": limit,
                    "depth": depth,
                    "include_clickstream_data": request.include_clickstream_data,
                    "closely_variants": request.closely_variants,
                    "ignore_synonyms": request.ignore_synonyms,
                }
                run_id = discovery_service.create_discovery_run(
                    client_id=client_id, parameters=parameters
                )

                job_id = orchestrator.run_discovery_and_save(
                    run_id,
                    request.seed_keywords,
                    discovery_modes,
                    filters,
                    request.order_by,
                    request.filters_override,
                    limit,
                    depth,
                    request.ignore_synonyms,
                    request.include_clickstream_data,
                    request.closely_variants,
                )
                return {"job_id": job_id, "message": f"Discovery run job {job_id} started."}
            except Exception as e:
                logger.error(
                    f"Failed to start discovery run for client {client_id}: {e}", exc_info=True
                )
                raise HTTPException(
                    status_code=500, detail=f"Failed to start discovery run: {e}"
                )
        ```
    *   **Reasoning:** This backend-only change implements the requested logic to intelligently select discovery modes based on the user's desired number of keywords, making the process more efficient without any frontend changes.

---

#### **Task 2: Implement Granular Job Progress Updates**

**Goal:** Provide users with clear, real-time feedback on which stage of the discovery process is currently running.

*   **Granular Task 2.1: Add Step Messages in the Backend Workflow**
    *   **File:** `pipeline/orchestrator/discovery_orchestrator.py`
    *   **Action:** In the `_run_discovery_background` function, add a `result={'step': '...'}` dictionary to the `update_job_status` calls.

    *   **Find this code block:**
        ```python
        job_status = self.job_manager.get_job_status(job_id)
        if job_status and job_status.get("status") == "failed":
            run_logger.warning(
                "Job found marked as 'failed' (cancelled). Exiting gracefully."
            )
            self.db_manager.update_discovery_run_status(run_id, "cancelled")
            return {"message": "Job cancelled by user request."}

        self.job_manager.update_job_status(
            job_id,
            "running",
            progress=10,
            result={"step": "Fetching & Scoring keywords"},
        )
        ```

    *   **Replace with this code block:**
        ```python
        job_status = self.job_manager.get_job_status(job_id)
        if job_status and job_status.get("status") == "failed":
            run_logger.warning(
                "Job found marked as 'failed' (cancelled). Exiting gracefully."
            )
            self.db_manager.update_discovery_run_status(run_id, "cancelled")
            return {"message": "Job cancelled by user request."}

        self.job_manager.update_job_status(
            job_id,
            "running",
            progress=10,
            result={"step": "Fetching Keywords from API..."},
        )
        ```

    *   **Action:** In the same function, find the next `update_job_status` call.
    *   **Find this code block:**
        ```python
        processed_opportunities = discovery_result.get("opportunities", [])

        self.job_manager.update_job_status(
            job_id, "running", progress=75, result={"step": "Saving to Database"}
        )

        num_added = 0
        ```
    *   **Replace with this code block:**
        ```python
        processed_opportunities = discovery_result.get("opportunities", [])

        self.job_manager.update_job_status(
            job_id, "running", progress=75, result={"step": "Saving Results to Database..."}
        )

        num_added = 0
        ```
*   **Granular Task 2.2: Display the Step Message on the Frontend**
    *   **File:** `src/pages/DiscoveryPage/components/DiscoveryHistory.jsx`
    *   **Action:** In the `columns` definition, modify the `Status` renderer to display the step message below the status tag for running jobs.

    *   **Find this code block:**
        ```javascript
        const progress = record.results_summary?.progress || (status === 'running' ? record.progress || 0 : 0);
        return (
          <div style={{ display: 'flex', alignItems: 'center', flexDirection: 'column' }}>
            <Tag icon={config.icon} color={config.color} onClick={() => status === 'failed' && handleShowError(record.error_message)} style={{ cursor: status === 'failed' ? 'pointer' : 'default', marginBottom: 4 }}>
              {config.text}
            </Tag>
            {status === 'running' && <Progress percent={progress} size="small" status="active" showInfo={false} style={{ width: 100 }} />}
          </div>
        );
        ```
    *   **Replace with this code block:**
        ```javascript
        const progress = record.results_summary?.progress || (status === 'running' ? record.progress || 0 : 0);
        const stepMessage = record.results_summary?.step || (status === 'running' ? 'Initializing...' : null);

        return (
          <div style={{ display: 'flex', alignItems: 'center', flexDirection: 'column', gap: '4px' }}>
            <Tag icon={config.icon} color={config.color} onClick={() => status === 'failed' && handleShowError(record.error_message)} style={{ cursor: status === 'failed' ? 'pointer' : 'default' }}>
              {config.text}
            </Tag>
            {status === 'running' && (
              <>
                <Text type="secondary" style={{ fontSize: '12px', fontStyle: 'italic' }}>{stepMessage}</Text>
                <Progress percent={progress} size="small" status="active" showInfo={false} style={{ width: 100, margin: 0 }} />
              </>
            )}
          </div>
        );
        ```    *   **Reasoning:** This provides immediate, valuable feedback to the user about the job's progress with minimal changes to the existing UI structure.

---

#### **Task 3: Optimize Job Status Polling**

**Goal:** Replace the inefficient list-wide polling with a more performant, React Query-native approach that only refetches when necessary.

*   **Granular Task 3.1: Modify the `useDiscoveryRuns` Hook**
    *   **File:** `src/pages/DiscoveryPage/hooks/useDiscoveryRuns.js`
    *   **Action:** Remove the entire `useEffect` block responsible for polling and replace it with a conditional `refetchInterval` in the `useQuery` options.

    *   **Find this code block:**
        ```javascript
        // Poll for updates on running jobs
        useEffect(() => {
          let intervalId;

          const checkRunningJobs = async () => {
            const currentRuns = queryClient.getQueryData(['discoveryRuns', clientId, page]);
            const runningRuns = currentRuns?.items?.filter(run => run.status === 'running' && run.job_id);

            if (!runningRuns || runningRuns.length === 0) {
              clearInterval(intervalId);
              intervalId = null;
              return;
            }

            let shouldRefetch = false;
            const statusChecks = runningRuns.map(run => getJobStatus(run.job_id));

            try {
              const jobStatuses = await Promise.all(statusChecks);
              if (jobStatuses.some(job => job.status === 'completed' || job.status === 'failed')) {
                shouldRefetch = true;
              }
            } catch (error) {
              console.error("Error polling job statuses:", error);
            }

            if (shouldRefetch) {
              queryClient.invalidateQueries(['discoveryRuns', clientId]);
            }
          };

          // Start polling only if there are running jobs initially
          const initialRunningRuns = data?.items?.filter(run => run.status === 'running' && run.job_id);
          if (initialRunningRuns && initialRunningRuns.length > 0 && !intervalId) {
            intervalId = setInterval(checkRunningJobs, 8000); // Poll every 8 seconds
          }

          return () => {
            if (intervalId) {
              clearInterval(intervalId);
            }
          };
        }, [data, clientId, queryClient, page]); // Add 'page' to dependencies
        ```
    *   **And this `useQuery` block:**
        ```javascript
        const {
          data,
          isLoading,
          isError,
          error,
          refetch, // Get the refetch function
        } = useQuery(
          ['discoveryRuns', clientId, page],
          () => getDiscoveryRuns(clientId, page),
          {
            enabled: !!clientId,
            keepPreviousData: true,
          }
        );
        ```

    *   **Replace both of the above blocks with this single, modified `useQuery` block:**
        ```javascript
        const {
          data,
          isLoading,
          isError,
          error,
        } = useQuery(
          ['discoveryRuns', clientId, page],
          () => getDiscoveryRuns(clientId, page),
          {
            enabled: !!clientId,
            keepPreviousData: true,
            // Automatically refetch the list every 8 seconds ONLY if there are jobs currently in a 'running' or 'pending' state.
            // This is much more efficient than the previous useEffect implementation.
            refetchInterval: (data) => {
              const isAnyJobRunning = data?.items?.some(run => run.status === 'running' || run.status === 'pending');
              return isAnyJobRunning ? 8000 : false;
            },
          }
        );
        ```
    *   **Reasoning:** This change leverages a built-in React Query feature (`refetchInterval`) to achieve the same goal as the complex `useEffect` hook, but in a much more efficient, declarative, and maintainable way. It eliminates the performance bottleneck and UI flicker.

---

### **Phase 2: Foundational Fixes**

#### **Task 4: Implement Backend-Powered Filtering for Discovery History**

**Goal:** Fix the broken search/filter functionality on the Discovery History page by moving the logic to the backend.

*   **Granular Task 4.1: Modify Backend API Endpoint**
    *   **File:** `api/routers/discovery.py`
    *   **Action:** Update the `get_discovery_runs` function signature to accept new filter parameters and pass them to the database manager.

    *   **Find this code block:**
        ```python
        @router.get("/clients/{client_id}/discovery-runs")
        async def get_discovery_runs(
            client_id: str,
            page: int = 1,
            limit: int = 10,
            db: DatabaseManager = Depends(get_db),
            orchestrator: WorkflowOrchestrator = Depends(get_orchestrator),
        ):
            if client_id != orchestrator.client_id:
                raise HTTPException(
                    status_code=403,
                    detail="You do not have permission to access this client's resources.",
                )
            runs, total_count = db.get_all_discovery_runs_paginated(client_id, page, limit)
            if not runs:
                return {"items": [], "total_items": 0, "page": page, "limit": limit}
            return {"items": runs, "total_items": total_count, "page": page, "limit": limit}
        ```

    *   **Replace with this code block:**
        ```python
        from typing import Optional

        @router.get("/clients/{client_id}/discovery-runs")
        async def get_discovery_runs(
            client_id: str,
            page: int = 1,
            limit: int = 10,
            search_query: Optional[str] = None,
            date_range_start: Optional[str] = None,
            date_range_end: Optional[str] = None,
            db: DatabaseManager = Depends(get_db),
            orchestrator: WorkflowOrchestrator = Depends(get_orchestrator),
        ):
            if client_id != orchestrator.client_id:
                raise HTTPException(
                    status_code=403,
                    detail="You do not have permission to access this client's resources.",
                )
            
            filters = {
                "search_query": search_query,
                "start_date": date_range_start,
                "end_date": date_range_end,
            }

            runs, total_count = db.get_all_discovery_runs_paginated(client_id, page, limit, filters)
            if not runs:
                return {"items": [], "total_items": 0, "page": page, "limit": limit}
            return {"items": runs, "total_items": total_count, "page": page, "limit": limit}
        ```

*   **Granular Task 4.2: Modify Database Query Function**
    *   **File:** `data_access/database_manager.py`
    *   **Action:** Update `get_all_discovery_runs_paginated` to build a dynamic `WHERE` clause based on the new filter parameters.

    *   **Find this code block:**
        ```python
        def get_all_discovery_runs_paginated(
            self, client_id: str, page: int, limit: int
        ) -> Tuple[List[Dict[str, Any]], int]:
            """Retrieves all discovery runs for a specific client with pagination."""
            conn = self._get_conn()
            with conn:
                cursor = conn.cursor()

                # Get total count
                cursor.execute(
                    "SELECT COUNT(*) FROM discovery_runs WHERE client_id = ?", (client_id,)
                )
                total_count = cursor.fetchone()[0]

                cursor.execute(
                    "SELECT * FROM discovery_runs WHERE client_id = ? ORDER BY start_time DESC LIMIT ? OFFSET ?",
                    (client_id, limit, (page - 1) * limit),
                )
                runs = []
                for row in cursor.fetchall():
                    run = dict(row)
                    try:
                        if run.get("parameters"):
                            run["parameters"] = json.loads(run["parameters"])
                        if run.get("results_summary"):
                            run["results_summary"] = json.loads(run["results_summary"])
                    except json.JSONDecodeError:
                        self.logger.warning(
                            f"Failed to parse JSON for discovery run ID {run.get('id')}."
                        )
                    runs.append(run)
                return runs, total_count
        ```

    *   **Replace with this code block:**
        ```python
        def get_all_discovery_runs_paginated(
            self, client_id: str, page: int, limit: int, filters: Optional[Dict[str, Any]] = None
        ) -> Tuple[List[Dict[str, Any]], int]:
            """Retrieves all discovery runs for a specific client with pagination and filtering."""
            conn = self._get_conn()
            
            base_query = "FROM discovery_runs WHERE client_id = ?"
            query_params = [client_id]
            
            where_clauses = []
            if filters:
                if filters.get("search_query"):
                    where_clauses.append("(parameters LIKE ? OR status LIKE ?)")
                    search_term = f"%{filters['search_query']}%"
                    query_params.extend([search_term, search_term])
                if filters.get("start_date") and filters.get("end_date"):
                    where_clauses.append("start_time BETWEEN ? AND ?")
                    query_params.extend([filters["start_date"], filters["end_date"]])

            if where_clauses:
                base_query += " AND " + " AND ".join(where_clauses)

            with conn:
                cursor = conn.cursor()
                
                # Get total count with filters
                count_query = f"SELECT COUNT(*) {base_query}"
                cursor.execute(count_query, query_params)
                total_count = cursor.fetchone()[0]
                
                # Get paginated data with filters
                select_query = f"SELECT * {base_query} ORDER BY start_time DESC LIMIT ? OFFSET ?"
                cursor.execute(select_query, query_params + [limit, (page - 1) * limit])
                
                runs = []
                for row in cursor.fetchall():
                    run = dict(row)
                    try:
                        if run.get("parameters"):
                            run["parameters"] = json.loads(run["parameters"])
                        if run.get("results_summary"):
                            run["results_summary"] = json.loads(run["results_summary"])
                    except json.JSONDecodeError:
                        self.logger.warning(
                            f"Failed to parse JSON for discovery run ID {run.get('id')}."
                        )
                    runs.append(run)
                return runs, total_count
        ```

*   **Granular Task 4.3: Update Frontend `useDiscoveryRuns` Hook**
    *   **File:** `src/pages/DiscoveryPage/hooks/useDiscoveryRuns.js`
    *   **Action:** Modify the hook to accept and pass filter state to the API.

    *   **Find this code block:**
        ```javascript
        export const useDiscoveryRuns = () => {
          const queryClient = useQueryClient();
          const { clientId } = useClient();
          const { showNotification } = useNotifications();
          const [page, setPage] = useState(1);

          // Query to fetch discovery run history
          const {
            data,
            isLoading,
            isError,
            error,
            refetch, // Get the refetch function
          } = useQuery(
            ['discoveryRuns', clientId, page],
            () => getDiscoveryRuns(clientId, page),
            {
              enabled: !!clientId,
              keepPreviousData: true,
            }
          );
        ```

    *   **Replace with this code block:**
        ```javascript
        export const useDiscoveryRuns = (searchQuery, dateRange) => { // Accept filters
          const queryClient = useQueryClient();
          const { clientId } = useClient();
          const { showNotification } = useNotifications();
          const [page, setPage] = useState(1);
        
          // Query to fetch discovery run history
          const {
            data,
            isLoading,
            isError,
            error,
          } = useQuery(
            // Add filters to the query key to trigger re-fetching on change
            ['discoveryRuns', clientId, page, searchQuery, dateRange],
            () => getDiscoveryRuns(clientId, page, { searchQuery, dateRange }), // Pass filters to API call
            {
              enabled: !!clientId,
              keepPreviousData: true,
              refetchInterval: (data) => {
                const isAnyJobRunning = data?.items?.some(run => run.status === 'running' || run.status === 'pending');
                return isAnyJobRunning ? 8000 : false;
              },
            }
          );
        ```

*   **Granular Task 4.4: Update Frontend `DiscoveryPage` and `DiscoveryHistory` Components**
    *   **Action:** Lift state for filters from `DiscoveryHistory` to `DiscoveryPage`.
    *   **File:** `src/pages/DiscoveryPage/DiscoveryPage.jsx`
    *   **Find this code block:**
        ```javascript
        const DiscoveryPage = () => {
          const { runs, isLoading, isError, error, startRunMutation, rerunMutation } = useDiscoveryRuns();
          const { clientId } = useClient();
          const navigate = useNavigate(); // Initialize navigate

          const handleRerun = (runId) => {
              rerunMutation.mutate(runId);
          }
        ```
    *   **Replace with this code block:**
        ```javascript
        import useDebounce from '../../hooks/useDebounce'; // Add this import

        const DiscoveryPage = () => {
          const [searchQuery, setSearchQuery] = useState('');
          const [dateRange, setDateRange] = useState(null);
          const debouncedSearchQuery = useDebounce(searchQuery, 500);

          const { runs, totalRuns, page, setPage, isLoading, isError, error, startRunMutation, rerunMutation } = useDiscoveryRuns(debouncedSearchQuery, dateRange);
          const { clientId } = useClient();
          const navigate = useNavigate(); // Initialize navigate
        
          const handleRerun = (runId) => {
              rerunMutation.mutate(runId);
          }
        ```
    *   **Action:** Pass state and handlers down to `DiscoveryHistory`.
    *   **File:** `src/pages/DiscoveryPage/DiscoveryPage.jsx`
    *   **Find this code block:**
        ```javascript
          <DiscoveryHistory
              runs={runs}
              isLoading={startRunMutation.isLoading || rerunMutation.isLoading}
              onRerun={handleRerun}
              isRerunning={rerunMutation.isLoading}
          />
        ```
    *   **Replace with this code block:**
        ```javascript
          <DiscoveryHistory
              runs={runs}
              totalRuns={totalRuns}
              page={page}
              setPage={setPage}
              isLoading={isLoading || startRunMutation.isLoading || rerunMutation.isLoading}
              onRerun={handleRerun}
              isRerunning={rerunMutation.isLoading}
              searchQuery={searchQuery}
              setSearchQuery={setSearchQuery}
              setDateRange={setDateRange}
          />
        ```

*   **Granular Task 4.5: Update `DiscoveryHistory.jsx` to Use Props**
    *   **File:** `src/pages/DiscoveryPage/components/DiscoveryHistory.jsx`
    *   **Action:** Remove local state for filters and use the props passed down from `DiscoveryPage`.

    *   **Find this code block:**
        ```javascript
        const DiscoveryHistory = ({ runs, totalRuns, page, setPage, isLoading, onRerun, isRerunning }) => {
          const navigate = useNavigate();
          const [filterText, setFilterText] = useState('');
          const [dateRange, setDateRange] = useState(null);
          const [errorModal, setErrorModal] = useState({ open: false, content: '' });
          const [detailsModal, setDetailsModal] = useState({ open: false, run: null });
        ```
    *   **Replace with this code block:**
        ```javascript
        const DiscoveryHistory = ({
          runs, totalRuns, page, setPage, isLoading, onRerun, isRerunning,
          searchQuery, setSearchQuery, setDateRange
        }) => {
          const navigate = useNavigate();
          // Local state for filters is removed, now using props
          const [errorModal, setErrorModal] = useState({ open: false, content: '' });
          const [detailsModal, setDetailsModal] = useState({ open: false, run: null });
        ```

    *   **Action:** Remove the `useMemo` for client-side filtering and update the input components.
    *   **File:** `src/pages/DiscoveryPage/components/DiscoveryHistory.jsx`
    *   **Find and DELETE this entire `useMemo` block:**
        ```javascript
        const filteredRuns = useMemo(() => {
          let filtered = runs;

          if (filterText) {
            const lowerCaseFilter = filterText.toLowerCase();
            filtered = filtered.filter(run => 
              run.parameters?.seed_keywords?.some(kw => kw.toLowerCase().includes(lowerCaseFilter)) || 
              run.status.toLowerCase().includes(lowerCaseFilter)
            );
          }

          if (dateRange) {
            const [start, end] = dateRange;
            filtered = filtered.filter(run => {
              const runDate = new Date(run.start_time);
              return runDate >= start && runDate <= end;
            });
          }

          return filtered;
        }, [runs, filterText, dateRange]);
        ```
    *   **Action:** Update the `Search` and `RangePicker` components to use the new props.
    *   **File:** `src/pages/DiscoveryPage/components/DiscoveryHistory.jsx`
    *   **Find this code block:**
        ```javascript
              <Search 
                placeholder="Filter by keyword or status..." 
                allowClear 
                value={filterText} 
                onChange={e => setFilterText(e.target.value)} 
                style={{ width: 250, marginRight: '8px' }} 
              />
              <RangePicker onChange={(dates) => setDateRange(dates)} />
        ```
    *   **Replace with this code block:**
        ```javascript
              <Search 
                placeholder="Filter by keyword or status..." 
                allowClear 
                value={searchQuery} 
                onChange={e => setSearchQuery(e.target.value)} 
                style={{ width: 250, marginRight: '8px' }} 
              />
              <RangePicker onChange={(dates) => {
                const dateStrings = dates ? [dates[0].toISOString(), dates[1].toISOString()] : null;
                setDateRange(dateStrings);
              }} />
        ```
    *   **Action:** Update the `Table` component to use `runs` directly instead of `filteredRuns`.
    *   **File:** `src/pages/DiscoveryPage/components/DiscoveryHistory.jsx`
    *   **Find this code block:**
        ```javascript
        <Table
          loading={isLoading}
          columns={columns}
          dataSource={filteredRuns}
        ```
    *   **Replace with this code block:**
        ```javascript
        <Table
          loading={isLoading}
          columns={columns}
          dataSource={runs}
        ```
    *   **Reasoning:** This set of granular tasks correctly moves filtering logic to the backend, fixing the bug while safely managing state between the necessary frontend components.

---

Excellent question. You are right to focus on the secondary effects of any code change. A well-designed implementation plan must account for these "ripple effects" to prevent new bugs from being introduced.

The 7-task plan was designed to be as low-risk as possible, but several of those tasks do require small, specific supporting actions to ensure they are implemented safely and completely.

Here is the exhaustive list of supporting tasks required to handle all ripple effects for the code updates in the main plan. These are the "housekeeping" and verification steps that ensure stability.

---

### **Supporting Tasks and Verifications for the Implementation Plan**

This section should be executed in conjunction with the main implementation plan.

#### **For Task 2: Implement Granular Progress Updates**

*   **Ripple Effect Analysis:** The primary change is adding a `step` message to the job's `result` object. While the Discovery Page will be updated to read this, other components like the main `ActivityLogPage` or the `WorkflowTracker` on the Opportunity Detail page might also display job statuses. They could show `[Object object]` or break if they don't handle the new data structure gracefully.
*   **Supporting Task(s):**
    1.  **Defensive Code in `JobStatusIndicator.jsx`:** This central component is used in multiple places. We must ensure it handles the new `step` message correctly and has a safe fallback.
        *   **File:** `src/components/JobStatusIndicator.jsx`
        *   **Action:** Find the `statusConfig` object.
        *   **Find this code block:**
            ```javascript
            running: { icon: <LoadingOutlined spin />, color: 'processing', text: job.result?.step || 'Running...' },
            ```
        *   **Verify:** The code already uses optional chaining (`?.`) and a fallback (`|| 'Running...'`). This is excellent defensive coding and is already safe. **No code change is needed, but this verification is a critical step.**

---

#### **For Task 3: Fix the Inefficient Status Polling**

*   **Ripple Effect Analysis:** The change to `useDiscoveryRuns.js` uses React Query's `refetchInterval` to re-poll the main list endpoint. The primary risk is ensuring this polling reliably stops.
*   **Supporting Task(s):**
    1.  **Manual E2E Verification:** After implementing the change, perform a manual test:
        *   Start a new discovery run.
        *   Open the browser's Developer Tools and go to the "Network" tab.
        *   Filter for requests to `discovery-runs`.
        *   Observe that a new request is made every 8 seconds while the job status is "running" or "pending".
        *   **Crucially, verify that after the job's status changes to "completed" or "failed", the network requests stop.** This confirms the fix is working as intended and not polling indefinitely.

---

#### **For Task 4: Implement Backend-Powered Filtering**

*   **Ripple Effect Analysis:** This task has the most moving parts. The implementation plan covered the core changes, but missed two important details: updating the frontend service layer and managing UI state correctly.
*   **Supporting Task(s):**
    1.  **Update Frontend API Service:** The `getDiscoveryRuns` function in the service layer must be updated to handle the new parameters.
        *   **File:** `src/services/discoveryService.js`
        *   **Find this function:**
            ```javascript
            export const getDiscoveryRuns = (clientId, page = 1) => {
              return apiClient.get(`/api/clients/${clientId}/discovery-runs`, { params: { page } });
            };
            ```
        *   **Replace with this:**
            ```javascript
            export const getDiscoveryRuns = (clientId, page = 1, filters = {}) => {
              const params = {
                page,
                search_query: filters.searchQuery || undefined,
                date_range_start: filters.dateRange ? filters.dateRange[0] : undefined,
                date_range_end: filters.dateRange ? filters.dateRange[1] : undefined,
              };
              return apiClient.get(`/api/clients/${clientId}/discovery-runs`, { params });
            };
            ```
    2.  **Reset Pagination on Filter Change:** To prevent a confusing user experience (e.g., being on page 5 of a now-empty filter result), the page number must be reset to 1 whenever a filter is applied.
        *   **File:** `src/pages/DiscoveryPage/DiscoveryPage.jsx`
        *   **Action:** Modify the state setters for the filters.
        *   **Find this line in the component:**
            ```javascript
            const { runs, totalRuns, page, setPage, isLoading, isError, error, startRunMutation, rerunMutation } = useDiscoveryRuns(debouncedSearchQuery, dateRange);
            ```
        *   **Add these two handler functions right below it:**
            ```javascript
            const handleSearchChange = (query) => {
              setSearchQuery(query);
              setPage(1); // Reset to first page on new search
            };

            const handleDateChange = (dates) => {
              setDateRange(dates);
              setPage(1); // Reset to first page on date change
            };
            ```
        *   **Action:** Pass these new handlers as props to `DiscoveryHistory`.
        *   **Find this code block:**
            ```javascript
              setSearchQuery={setSearchQuery}
              setDateRange={setDateRange}
            ```
        *   **Replace with this:**
            ```javascript
              setSearchQuery={handleSearchChange}
              setDateRange={handleDateChange}
            ```        *   **Action:** Finally, update `DiscoveryHistory.jsx` to use these new handlers.
        *   **File:** `src/pages/DiscoveryPage/components/DiscoveryHistory.jsx`
        *   **Find and replace the `onChange` handlers for the `Search` and `RangePicker` components with this:**
            ```javascript
                  <Search 
                    placeholder="Filter by keyword or status..." 
                    allowClear 
                    value={searchQuery} 
                    onChange={e => setSearchQuery(e.target.value)} 
                    style={{ width: 250, marginRight: '8px' }} 
                  />
                  <RangePicker onChange={(dates) => {
                    const dateStrings = dates ? [dates[0].toISOString(), dates[1].toISOString()] : null;
                    setDateRange(dateStrings);
                  }} />
            ```

---

#### **For Task 6: Implement Incremental Saving in the Workflow**

*   **Ripple Effect Analysis:** This change introduces a new temporary status (e.g., "fetched") for opportunities. If the job fails during the subsequent scoring phase, these records will be left in the database in this intermediate state. They are effectively "orphaned."
*   **Supporting Task(s):**
    1.  **Implement a Status for Post-Fetch Failures:** The system needs a way to handle records that fail *after* being saved. The best approach is to add a new final status.
        *   **File:** `pipeline/orchestrator/discovery_orchestrator.py`
        *   **Action:** Inside the `_run_discovery_background` function's `try...except` block, if an error occurs *after* the initial save, you must loop through the "fetched" records for that `run_id` and update their status to "failed_scoring".
        *   **Add this logic to the `except` block:**
            ```python
            except Exception as e:
                error_message = f"Discovery workflow failed: {e}\n{traceback.format_exc()}"
                run_logger.error(error_message)
                self.db_manager.update_discovery_run_failed(run_id, str(e))
                self.job_manager.update_job_status(
                    job_id, "failed", progress=100, error=str(e)
                )
                # --- ADD THIS NEW BLOCK ---
                # Mark any partially processed opportunities from this run as failed.
                run_logger.info(f"Marking partially fetched opportunities from run_id {run_id} as 'failed_scoring'.")
                conn = self.db_manager._get_conn()
                with conn:
                    conn.execute(
                        "UPDATE opportunities SET status = 'failed_scoring', error_message = ? WHERE run_id = ? AND status = 'fetched'",
                        (f"Parent discovery job {job_id} failed.", run_id)
                    )
                # --- END NEW BLOCK ---
                raise
            ```
    *   **This ensures that no records are left in an ambiguous intermediate state.** They will be clearly marked as having failed during the processing stage.

---
Of course. This is an excellent and crucial step. A successful implementation isn't just about making the primary code changes; it's about anticipating and handling all the secondary effects to ensure nothing else breaks.

The initial plan was designed to be low-risk, but several tasks require small, specific supporting actions to be fully "safe" and complete. Here is the exhaustive list of these additional tasks required to handle all ripple effects.

This revised plan is designed to be executed by an AI coding agent, leaving no room for ambiguity.

---

### **Complete Implementation Plan: Supporting Tasks for Stability**

**Objective:** To supplement the main implementation plan by explicitly defining the verification steps and minor code changes required to mitigate all potential side effects of the primary tasks.

---

#### **Supporting Tasks for Phase 1: Critical Backend Performance Optimization**

These tasks ensure that the performance fixes do not break functionality for older data records.

*   **Task Group 1 (Associated with Optimizing Database Sorting)**
    *   **Granular Task 1.1: Verify Data Integrity of Promoted Columns**
        *   **Action Type:** Verification (Non-Coding)
        *   **Instructions:** Before deploying the backend changes, the developer must connect to the SQLite database (`data/opportunities.db`) using a database client. They must run the following queries to verify that the primary sorting columns are correctly populated for *all* records:
            ```sql
            -- Check for any records where search_volume might be null or zero
            SELECT id, keyword, search_volume FROM opportunities WHERE search_volume IS NULL OR search_volume = 0 LIMIT 10;

            -- Check for any records where keyword_difficulty might be null
            SELECT id, keyword, keyword_difficulty FROM opportunities WHERE keyword_difficulty IS NULL LIMIT 10;
            ```
        *   **Reasoning:** The optimization relies on these columns having correct data. The application's data migration and deserialization logic is supposed to handle this, but this manual check provides a final guarantee that sorting will be accurate for both historical and new data.

---

#### **Supporting Tasks for Phase 2: API and Frontend Data Handling**

These tasks ensure the frontend correctly adapts to the consolidated API response.

*   **Task Group 2 (Associated with Consolidating API Calls)**
    *   **Granular Task 2.1: Verify API Response Shape**
        *   **Action Type:** Verification (Non-Coding)
        *   **Instructions:** After implementing the backend changes, use a tool like Postman or the browser's Network tab to inspect the response from the `GET /api/clients/{client_id}/opportunities` endpoint. Confirm that the JSON response body now includes a `status_counts` object with the correct structure, for example:
            ```json
            {
              "items": [...],
              "total_items": 100,
              "page": 1,
              "limit": 20,
              "status_counts": {
                "review": 50,
                "generated": 25,
                "rejected": 25
              }
            }
            ```
        *   **Reasoning:** This confirms that the backend contract has been updated correctly before the frontend code is modified to consume it, preventing integration bugs.

---

#### **Supporting Tasks for Phase 3: Core UI and State Management Refactor**

These tasks add robustness to the new UI features and state management logic.

*   **Task Group 3 (Associated with Implementing Search)**
    *   **Granular Task 3.1: Make Backend Search Case-Insensitive**
        *   **File:** `data_access/database_manager.py`
        *   **Action:** Modify the `get_all_opportunities` function to use the `LOWER()` SQL function to ensure case-insensitive searching.
        *   **Find this code block:**
            ```python
            if params.get("keyword"):
                where_parts.append("keyword LIKE ?")
                query_values.append(f'%{params["keyword"]}%')
            ```
        *   **Replace with this code block:**
            ```python
            if params.get("keyword"):
                where_parts.append("LOWER(keyword) LIKE LOWER(?)")
                query_values.append(f'%{params["keyword"]}%')
            ```
        *   **Reasoning:** This provides a better user experience, as users expect a search for "marketing" to also find "Marketing".

*   **Task Group 4 (Associated with Fixing Job Polling)**
    *   **Granular Task 4.1: Verify Presence of `latest_job_id`**
        *   **Action Type:** Verification (Non-Coding)
        *   **Instructions:** Inspect the JSON response from the `GET /api/clients/{client_id}/opportunities` endpoint. Confirm that each opportunity object in the `items` array includes the `latest_job_id` field (it can be `null`, but the key must be present).
        *   **Reasoning:** The `JobStatusIndicator` component relies on this ID to function. This step confirms that the necessary data is being provided by the API before the frontend component is integrated.

    *   **Granular Task 4.2: Manually Verify Polling Stops**
        *   **Action Type:** E2E Test (Non-Coding)
        *   **Instructions:** After all frontend and backend changes are deployed, perform the following manual test:
            1.  Open the Opportunities Page in the browser.
            2.  Open the browser's Developer Tools and select the "Network" tab.
            3.  Start a new workflow for an opportunity.
            4.  In the Network tab, observe that a request to the `/api/clients/.../opportunities` endpoint is made every 5 seconds.
            5.  Wait for the job to complete (its status changes from "Running" to "Paused" or "Generated").
            6.  **Crucially, confirm that the 5-second polling requests immediately stop.**
        *   **Reasoning:** This is the most important verification step. It proves that the `refetchInterval` logic is working correctly and that the application is not stuck in an infinite loop of network requests, which would degrade performance and increase server costs.

        Of course. This is an excellent and crucial step. A successful implementation isn't just about making the primary code changes; it's about anticipating and handling all the secondary effects to ensure nothing else breaks.

The initial plan was designed to be low-risk, but several tasks require small, specific supporting actions to be fully "safe" and complete. Here is the exhaustive list of these additional tasks required to handle all ripple effects.

This revised plan is designed to be executed by an AI coding agent, leaving no room for ambiguity.

---

### **Complete Implementation Plan: Supporting Tasks for Stability**

**Objective:** To supplement the main implementation plan by explicitly defining the verification steps and minor code changes required to mitigate all potential side effects of the primary tasks.

---

#### **Supporting Tasks for Phase 1: Critical Backend Performance Optimization**

These tasks ensure that the performance fixes do not break functionality for older data records.

*   **Task Group 1 (Associated with Optimizing Database Sorting)**
    *   **Granular Task 1.1: Verify Data Integrity of Promoted Columns**
        *   **Action Type:** Verification (Non-Coding)
        *   **Instructions:** Before deploying the backend changes, the developer must connect to the SQLite database (`data/opportunities.db`) using a database client. They must run the following queries to verify that the primary sorting columns are correctly populated for *all* records:
            ```sql
            -- Check for any records where search_volume might be null or zero
            SELECT id, keyword, search_volume FROM opportunities WHERE search_volume IS NULL OR search_volume = 0 LIMIT 10;

            -- Check for any records where keyword_difficulty might be null
            SELECT id, keyword, keyword_difficulty FROM opportunities WHERE keyword_difficulty IS NULL LIMIT 10;
            ```
        *   **Reasoning:** The optimization relies on these columns having correct data. The application's data migration and deserialization logic is supposed to handle this, but this manual check provides a final guarantee that sorting will be accurate for both historical and new data.

---

#### **Supporting Tasks for Phase 2: API and Frontend Data Handling**

These tasks ensure the frontend correctly adapts to the consolidated API response.

*   **Task Group 2 (Associated with Consolidating API Calls)**
    *   **Granular Task 2.1: Verify API Response Shape**
        *   **Action Type:** Verification (Non-Coding)
        *   **Instructions:** After implementing the backend changes, use a tool like Postman or the browser's Network tab to inspect the response from the `GET /api/clients/{client_id}/opportunities` endpoint. Confirm that the JSON response body now includes a `status_counts` object with the correct structure, for example:
            ```json
            {
              "items": [...],
              "total_items": 100,
              "page": 1,
              "limit": 20,
              "status_counts": {
                "review": 50,
                "generated": 25,
                "rejected": 25
              }
            }
            ```
        *   **Reasoning:** This confirms that the backend contract has been updated correctly before the frontend code is modified to consume it, preventing integration bugs.

---

#### **Supporting Tasks for Phase 3: Core UI and State Management Refactor**

These tasks add robustness to the new UI features and state management logic.

*   **Task Group 3 (Associated with Implementing Search)**
    *   **Granular Task 3.1: Make Backend Search Case-Insensitive**
        *   **File:** `data_access/database_manager.py`
        *   **Action:** Modify the `get_all_opportunities` function to use the `LOWER()` SQL function to ensure case-insensitive searching.
        *   **Find this code block:**
            ```python
            if params.get("keyword"):
                where_parts.append("keyword LIKE ?")
                query_values.append(f'%{params["keyword"]}%')
            ```
        *   **Replace with this code block:**
            ```python
            if params.get("keyword"):
                where_parts.append("LOWER(keyword) LIKE LOWER(?)")
                query_values.append(f'%{params["keyword"]}%')
            ```
        *   **Reasoning:** This provides a better user experience, as users expect a search for "marketing" to also find "Marketing".

*   **Task Group 4 (Associated with Fixing Job Polling)**
    *   **Granular Task 4.1: Verify Presence of `latest_job_id`**
        *   **Action Type:** Verification (Non-Coding)
        *   **Instructions:** Inspect the JSON response from the `GET /api/clients/{client_id}/opportunities` endpoint. Confirm that each opportunity object in the `items` array includes the `latest_job_id` field (it can be `null`, but the key must be present).
        *   **Reasoning:** The `JobStatusIndicator` component relies on this ID to function. This step confirms that the necessary data is being provided by the API before the frontend component is integrated.

    *   **Granular Task 4.2: Manually Verify Polling Stops**
        *   **Action Type:** E2E Test (Non-Coding)
        *   **Instructions:** After all frontend and backend changes are deployed, perform the following manual test:
            1.  Open the Opportunities Page in the browser.
            2.  Open the browser's Developer Tools and select the "Network" tab.
            3.  Start a new workflow for an opportunity.
            4.  In the Network tab, observe that a request to the `/api/clients/.../opportunities` endpoint is made every 5 seconds.
            5.  Wait for the job to complete (its status changes from "Running" to "Paused" or "Generated").
            6.  **Crucially, confirm that the 5-second polling requests immediately stop.**
        *   **Reasoning:** This is the most important verification step. It proves that the `refetchInterval` logic is working correctly and that the application is not stuck in an infinite loop of network requests, which would degrade performance and increase server costs.