# Critical Linting and Type Checking Issues

This report summarizes the critical issues found by `ruff`, `mypy`, and `eslint`.

## Ruff

| File | Line | Code | Message |
|---|---|---|---|
| /Users/ishtiaqbhatti/Desktop/clients/production/lark_app/backend/api/main.py | 13 | E402 | Module level import not at top of file |
| /Users/ishtiaqbhatti/Desktop/clients/production/lark_app/backend/api/main.py | 14 | E402 | Module level import not at top of file |
| /Users/ishtiaqbhatti/Desktop/clients/production/lark_app/backend/api/main.py | 15 | E402 | Module level import not at top of file |
| /Users/ishtiaqbhatti/Desktop/clients/production/lark_app/backend/api/main.py | 17 | E402 | Module level import not at top of file |
| /Users/ishtiaqbhatti/Desktop/clients/production/lark_app/backend/api/routers/client_settings.py | 11 | F821 | Undefined name `APIRouter` |
| /Users/ishtiaqbhatti/Desktop/clients/production/lark_app/backend/api/routers/client_settings.py | 17 | F821 | Undefined name `Depends` |
| /Users/ishtiaqbhatti/Desktop/clients/production/lark_app/backend/api/routers/client_settings.py | 18 | F821 | Undefined name `Depends` |
| /Users/ishtiaqbhatti/Desktop/clients/production/lark_app/backend/api/routers/client_settings.py | 21 | F821 | Undefined name `HTTPException` |
| /Users/ishtiaqbhatti/Desktop/clients/production/lark_app/backend/api/routers/client_settings.py | 27 | F821 | Undefined name `HTTPException` |
| /Users/ishtiaqbhatti/Desktop/clients/production/lark_app/backend/api/routers/client_settings.py | 37 | F821 | Undefined name `Depends` |
| /Users/ishtiaqbhatti/Desktop/clients/production/lark_app/backend/api/routers/client_settings.py | 38 | F821 | Undefined name `Depends` |
| /Users/ishtiaqbhatti/Desktop/clients/production/lark_app/backend/api/routers/client_settings.py | 41 | F821 | Undefined name `HTTPException` |
| /Users/ishtiaqbhatti/Desktop/clients/production/lark_app/backend/api/routers/client_settings.py | 53 | F821 | Undefined name `HTTPException` |
| /Users/ishtiaqbhatti/Desktop/clients/production/lark_app/backend/export_db.py | 9 | E402 | Module level import not at top of file |
| /Users/ishtiaqbhatti/Desktop/clients/production/lark_app/backend/export_db.py | 10 | E402 | Module level import not at top of file |
| /Users/ishtiaqbhatti/Desktop/clients/production/lark_app/backend/jobs.py | 77 | F821 | Undefined name `json` |
| /Users/ishtiaqbhatti/Desktop/clients/production/lark_app/backend/jobs.py | 78 | F821 | Undefined name `json` |

## mypy

| File | Line | Level | Message |
|---|---|---|---|
| backend/pipeline/step_01_discovery/disqualification_rules.py | 409 | SyntaxWarning | invalid escape sequence '\d' |

## ESLint

| File | Line | Column | Rule ID | Message |
|---|---|---|---|---|
| /Users/ishtiaqbhatti/Desktop/clients/production/lark_app/client/my-content-app/src/App.jsx | 20 | 10 | no-unused-vars | 'JobProvider' is defined but never used. |
| /Users/ishtiaqbhatti/Desktop/clients/production/lark_app/client/my-content-app/src/components/CostConfirmationModal.jsx | 7 | 9 | no-unused-vars | 'Title' is assigned a value but never used. |
| /Users/ishtiaqbhatti/Desktop/clients/production/lark_app/client/my-content-app/src/components/GlobalJobTracker.jsx | 4 | 10 | no-unused-vars | 'CheckCircleOutlined' is defined but never used. |
| /Users/ishtiaqbhatti/Desktop/clients/production/lark_app/client/my-content-app/src/components/GlobalJobTracker.jsx | 4 | 52 | no-unused-vars | 'LoadingOutlined' is defined but never used. |
| /Users/ishtiaqbhatti/Desktop/clients/production/lark_app/client/my-content-app/src/pages/DiscoveryPage/DiscoveryPage.jsx | 2 | 58 | no-unused-vars | 'message' is defined but never used. |
| /Users/ishtiaqbhatti/Desktop/clients/production/lark_app/client/my-content-app/src/pages/DiscoveryPage/DiscoveryPage.jsx | 8 | 8 | no-unused-vars | 'CostConfirmationModal' is defined but never used. |
| /Users/ishtiaqbhatti/Desktop/clients/production/lark_app/client/my-content-app/src/pages/DiscoveryPage/DiscoveryPage.jsx | 9 | 10 | no-unused-vars | 'estimateActionCost' is defined but never used. |
| /Users/ishtiaqbhatti/Desktop/clients/production/lark_app/client/my-content-app/src/pages/DiscoveryPage/DiscoveryPage.jsx | 23 | 9 | no-unused-vars | 'navigate' is assigned a value but never used. |
| /Users/ishtiaqbhatti/Desktop/clients/production/lark_app/client/my-content-app/src/pages/DiscoveryPage/components/DiscoveryForm.jsx | 2 | 74 | no-unused-vars | 'Card' is defined but never used. |
| /Users/ishtiaqbhatti/Desktop/clients/production/lark_app/client/my-content-app/src/pages/DiscoveryPage/components/DiscoveryHistory.jsx | 1 | 27 | no-unused-vars | 'useMemo' is defined but never used. |
| /Users/ishtiaqbhatti/Desktop/clients/production/lark_app/client/my-content-app/src/pages/DiscoveryPage/components/DiscoveryHistory.jsx | 2 | 104 | no-unused-vars | 'Alert' is defined but never used. |
| /Users/ishtiaqbhatti/Desktop/clients/production/lark_app/client/my-content-app/src/pages/DiscoveryPage/components/DiscoveryHistory.jsx | 3 | 10 | no-unused-vars | 'ReloadOutlined' is defined but never used. |
| /Users/ishtiaqbhatti/Desktop/clients/production/lark_app/client/my-content-app/src/pages/DiscoveryPage/components/DiscoveryHistory.jsx | 21 | 46 | no-unused-vars | 'onRerun' is defined but never used. |
| /Users/ishtiaqbhatti/Desktop/clients/production/lark_app/client/my-content-app/src/pages/DiscoveryPage/components/DiscoveryHistory.jsx | 21 | 55 | no-unused-vars | 'isRerunning' is defined but never used. |
| /Users/ishtiaqbhatti/Desktop/clients/production/lark_app/client/my-content-app/src/pages/DiscoveryPage/components/DiscoveryStatsBreakdown.jsx | 7 | 9 | no-unused-vars | 'Title' is assigned a value but never used. |
| /Users/ishtiaqbhatti/Desktop/clients/production/lark_app/client/my-content-app/src/pages/DiscoveryPage/components/DiscoveryStatsBreakdown.jsx | 7 | 16 | no-unused-vars | 'Text' is assigned a value but never used. |
| /Users/ishtiaqbhatti/Desktop/clients/production/lark_app/client/my-content-app/src/pages/DiscoveryPage/hooks/useDiscoveryRuns.js | 1 | 20 | no-unused-vars | 'useEffect' is defined but never used. |
| /Users/ishtiaqbhatti/Desktop/clients/production/lark_app/client/my-content-app/src/pages/DiscoveryPage/hooks/useDiscoveryRuns.js | 7 | 3 | no-unused-vars | 'getJobStatus' is defined but never used. |
| /Users/ishtiaqbhatti/Desktop/clients/production/lark_app/client/my-content-app/src/pages/OpportunitiesPage/OpportunitiesPage.jsx | 47 | 33 | no-unused-vars | 'opportunityKeyword' is defined but never used. |
| /Users/ishtiaqbhatti/Desktop/clients/production/lark_app/client/my-content-app/src/pages/OpportunitiesPage/hooks/useOpportunities.test.js | 6 | 1 | no-undef | 'jest' is not defined. |
| /Users/ishtiaqbhatti/Desktop/clients/production/lark_app/client/my-content-app/src/pages/OpportunitiesPage/hooks/useOpportunities.test.js | 11 | 10 | react/display-name | Component definition is missing display name |
| /Users/ishtiaqbhatti/Desktop/clients/production/lark_app/client/my-content-app/src/pages/OpportunitiesPage/hooks/useOpportunities.test.js | 12 | 5 | react/react-in-jsx-scope | 'React' must be in scope when using JSX |
| /Users/ishtiaqbhatti/Desktop/clients/production/lark_app/client/my-content-app/src/pages/OpportunitiesPage/hooks/useOpportunities.test.js | 16 | 1 | no-undef | 'test' is not defined. |
| /Users/ishtiaqbhatti/Desktop/clients/production/lark_app/client/my-content-app/src/pages/OpportunitiesPage/hooks/useOpportunities.test.js | 26 | 3 | no-undef | 'expect' is not defined. |
| /Users/ishtiaqbhatti/Desktop/clients/production/lark_app/client/my-content-app/src/pages/OpportunitiesPage/hooks/useOpportunities.test.js | 26 | 49 | no-undef | 'expect' is not defined. |
| /Users/ishtiaqbhatti/Desktop/clients/production/lark_app/client/my-content-app/src/pages/OpportunitiesPage/hooks/useOpportunities.test.js | 26 | 69 | no-undef | 'expect' is not defined. |
| /Users/ishtiaqbhatti/Desktop/clients/production/lark_app/client/my-content-app/src/pages/RunDetailsPage/RunDetailsPage.jsx | 4 | 43 | no-unused-vars | 'Progress' is defined but never used. |
| /Users/ishtiaqbhatti/Desktop/clients/production/lark_app/client/my-content-app/src/pages/Settings/SettingsPage.jsx | 2 | 27 | no-unused-vars | 'useEffect' is defined but never used. |
| /Users/ishtiaqbhatti/Desktop/clients/production/lark_app/client/my-content-app/src/pages/Settings/SettingsPage.jsx | 14 | 16 | no-unused-vars | 'Text' is assigned a value but never used. |
| /Users/ishtiaqbhatti/Desktop/clients/production/lark_app/client/my-content-app/src/pages/Settings/SettingsPage.jsx | 17 | 31 | no-unused-vars | 'settings' is defined but never used. |
| /Users/ishtiaqbhatti/Desktop/clients/production/lark_app/client/my-content-app/src/pages/Settings/SettingsPage.jsx | 17 | 41 | no-unused-vars | 'form' is defined but never used. |
| /Users/ishtiaqbhatti/Desktop/clients/production/lark_app/client/my-content-app/src/pages/Settings/SettingsPage.jsx | 27 | 61 | no-unused-vars | 'refetch' is assigned a value but never used. |
| /Users/ishtiaqbhatti/Desktop/clients/production/lark_app/client/my-content-app/src/pages/Settings/tabs/AiContentSettingsTab.jsx | 7 | 16 | no-unused-vars | 'Text' is assigned a value but never used. |
| /Users/ishtiaqbhatti/Desktop/clients/production/lark_app/client/my-content-app/src/pages/Settings/tabs/AiContentSettingsTab.jsx | 10 | 33 | no-unused-vars | 'settings' is defined but never used. |
| /Users/ishtiaqbhatti/Desktop/clients/production/lark_app/client/my-content-app/src/pages/Settings/tabs/DiscoverySettingsTab.jsx | 6 | 16 | no-unused-vars | 'Text' is assigned a value but never used. |
| /Users/ishtiaqbhatti/Desktop/clients/production/lark_app/client/my-content-app/src/pages/Settings/tabs/DiscoverySettingsTab.jsx | 9 | 33 | no-unused-vars | 'settings' is defined but never used. |
| /Users/ishtiaqbhatti/Desktop/clients/production/lark_app/client/my-content-app/src/pages/Settings/tabs/DiscoverySettingsTab.jsx | 9 | 43 | no-unused-vars | 'form' is defined but never used. |
| /Users/ishtiaqbhatti/Desktop/clients/production/lark_app/client/my-content-app/src/pages/Settings/tabs/ScoringWeightsTab.jsx | 6 | 16 | no-unused-vars | 'Text' is assigned a value but never used. |
| /Users/ishtiaqbhatti/Desktop/clients/production/lark_app/client/my-content-app/src/pages/Settings/tabs/ScoringWeightsTab.jsx | 8 | 30 | no-unused-vars | 'settings' is defined but never used. |
| /Users/ishtiaqbhatti/Desktop/clients/production/lark_app/client/my-content-app/src/pages/opportunity-detail-page/components/AdditionalInsights.jsx | 2 | 34 | no-unused-vars | 'Tag' is defined but never used. |
| /Users/ishtiaqbhatti/Desktop/clients/production/lark_app/client/my-content-app/src/pages/opportunity-detail-page/components/AdditionalInsights.jsx | 4 | 16 | no-unused-vars | 'Paragraph' is assigned a value but never used. |
