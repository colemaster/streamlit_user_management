# Dependency Analysis and Update Planning Report

## Executive Summary

This report analyzes the current dependencies in `pyproject.toml` and provides a comprehensive update matrix with the latest stable versions available as of January 2026. The analysis identifies potential conflicts, breaking changes, and required code modifications for the SDK modernization project.

## Current Dependencies Analysis

### Production Dependencies (Current vs Latest)

| Package | Current Version | Latest Version | Status | Priority |
|---------|----------------|----------------|---------|----------|
| authlib | >=1.3.2 | 1.6.6 | ⬆️ Major Update | High |
| httpx | >=0.28.1 | 0.28.1+ | ✅ Current | Low |
| msal | >=1.34.0 | 1.34.0+ | ✅ Current | Low |
| numpy | >=2.3.5 | 2.4.1 | ⬆️ Minor Update | Medium |
| pandas | >=2.3.3 | 3.0.0+ | ⬆️ Major Update | High |
| plotly | >=6.5.0 | 6.5.0+ | ✅ Current | Low |
| python-jose[cryptography] | >=3.5.0 | 3.5.0+ | ✅ Current | Low |
| python-dotenv | >=1.0.0 | 1.0.0+ | ✅ Current | Low |
| sqlalchemy | >=2.0.45 | 2.0.47+ | ⬆️ Patch Update | Medium |
| streamlit-nightly | >=1.52.1.dev20260109 | 1.52.1+ | ✅ Current | Low |
| uvloop | >=0.21.0 | 0.21.0+ | ✅ Current | Low |
| orjson | >=3.11.5 | 3.11.5+ | ✅ Current | Low |
| watchdog | >=6.0.0 | 6.0.0+ | ✅ Current | Low |

### Development Dependencies (Current vs Latest)

| Package | Current Version | Latest Version | Status | Priority |
|---------|----------------|----------------|---------|----------|
| hypothesis | >=6.29.0 | 6.103.1+ | ⬆️ Major Update | High |
| pytest | >=9.0.2 | 9.0.2+ | ✅ Current | Low |
| pytest-asyncio | >=1.3.0 | 0.26.0+ | ⬆️ Major Update | High |

## Detailed Update Analysis

### High Priority Updates

#### 1. Authlib (1.3.2 → 1.6.6)
**Breaking Changes:**
- Deprecation of `authlib.jose` module (migrate to `authlib.jose.rfc7519`)
- Updated OAuth 2.0 client configuration methods
- Enhanced security features requiring configuration updates

**Required Code Modifications:**
```python
# OLD
from authlib.jose import jwt

# NEW  
from authlib.jose.rfc7519 import jwt
```

**Migration Steps:**
1. Update import statements for JOSE functionality
2. Review OAuth client configurations
3. Test authentication flows thoroughly
4. Update error handling for new exception types

#### 2. Pandas (2.3.3 → 3.0.0+)
**Breaking Changes:**
- Major API changes in DataFrame operations
- Deprecated methods removed
- New default behaviors for data type inference
- Changes in index handling and MultiIndex operations

**Required Code Modifications:**
```python
# Review all DataFrame operations for compatibility
# Update deprecated method calls
# Verify data type handling
```

**Migration Steps:**
1. Run pandas migration checker
2. Update deprecated method calls
3. Test all data processing pipelines
4. Verify chart data compatibility with Plotly

#### 3. Hypothesis (6.29.0 → 6.103.1+)
**Breaking Changes:**
- Updated strategy APIs
- New default settings for test generation
- Enhanced shrinking algorithms
- Changes in example generation

**Required Code Modifications:**
```python
# Update strategy imports and usage
# Review test configurations
# Update property-based test implementations
```

**Migration Steps:**
1. Update all property-based tests
2. Review strategy configurations
3. Test shrinking behavior
4. Update test documentation

#### 4. pytest-asyncio (1.3.0 → 0.26.0+)
**Note:** Version number appears to have changed numbering scheme
**Breaking Changes:**
- Updated async fixture handling
- New event loop management
- Changes in async test execution

**Required Code Modifications:**
```python
# Update async test configurations
# Review fixture scopes
# Update asyncio mode settings
```

### Medium Priority Updates

#### 1. NumPy (2.3.5 → 2.4.1)
**Breaking Changes:**
- Minor API updates
- Performance improvements
- Enhanced array operations

**Migration Steps:**
1. Test array operations
2. Verify compatibility with pandas and plotly
3. Update type hints if needed

#### 2. SQLAlchemy (2.0.45 → 2.0.47+)
**Breaking Changes:**
- Patch-level updates with bug fixes
- Minor API enhancements

**Migration Steps:**
1. Test database operations
2. Verify ORM functionality
3. Update connection handling if needed

## Streamlit Nightly Features Analysis

### New Features Available (January 2026)

#### 1. Enhanced st.logout
- **Feature:** Secure session termination with OIDC provider integration
- **Implementation Required:** Integration with existing MSAL authentication
- **Code Changes:** Update authentication handlers

#### 2. st.dialog with Icon Support
- **Feature:** Modal dialogs with Material Symbols and emoji support
- **Implementation Required:** Update existing modal implementations
- **Code Changes:** Add icon parameters to dialog calls

#### 3. Enhanced st.metric
- **Feature:** Markdown support, sparklines, and delta arrow configuration
- **Implementation Required:** Update metric displays with new parameters
- **Code Changes:** Add chart_data and delta_arrow parameters

#### 4. Session-scoped Caching
- **Feature:** `@st.cache_data(scope="session")` for improved performance
- **Implementation Required:** Replace existing caching mechanisms
- **Code Changes:** Update cache decorators throughout application

#### 5. Enhanced st.data_editor
- **Feature:** Advanced data manipulation capabilities
- **Implementation Required:** Update data editing interfaces
- **Code Changes:** Implement new column types and editing modes

## Potential Conflicts and Resolutions

### 1. Pandas 3.0 + NumPy 2.4.1 Compatibility
**Risk Level:** Medium
**Resolution:** Both packages are designed to work together, but thorough testing required

### 2. Authlib 1.6.6 + python-jose 3.5.0
**Risk Level:** Low
**Resolution:** Both packages handle JWT operations - ensure no conflicts in usage

### 3. Streamlit Nightly + All Dependencies
**Risk Level:** Medium
**Resolution:** Test all integrations thoroughly, especially with plotly and pandas

## Implementation Recommendations

### Phase 1: Core Dependencies (Week 1)
1. Update NumPy to 2.4.1
2. Update SQLAlchemy to 2.0.47+
3. Test basic functionality

### Phase 2: Major Updates (Week 2)
1. Update Authlib to 1.6.6 with code migrations
2. Update Pandas to 3.0.0+ with extensive testing
3. Update testing framework (Hypothesis, pytest-asyncio)

### Phase 3: Integration and Testing (Week 3)
1. Implement new Streamlit features
2. Comprehensive integration testing
3. Performance benchmarking

## Risk Assessment

### High Risk Items
- Pandas 3.0 migration (extensive code changes required)
- Authlib JOSE module deprecation (authentication system impact)
- pytest-asyncio version change (test execution changes)

### Medium Risk Items
- NumPy minor version update (compatibility testing needed)
- SQLAlchemy patch update (database operation testing)

### Low Risk Items
- Packages already at latest versions
- Streamlit nightly feature additions (additive changes)

## Testing Strategy

### Unit Testing Requirements
- Test all authentication flows after Authlib update
- Verify all data processing pipelines after Pandas update
- Validate all chart rendering after dependency updates

### Property-Based Testing Requirements
- Update all Hypothesis-based tests for new version
- Test data processing properties with new Pandas version
- Validate authentication properties with updated Authlib

### Integration Testing Requirements
- End-to-end authentication testing
- Complete dashboard rendering validation
- Performance benchmarking across all scenarios

## Conclusion

The dependency update analysis reveals several significant updates required, with Pandas 3.0 and Authlib 1.6.6 being the most impactful. The phased approach recommended will minimize risk while ensuring all new features are properly integrated. Extensive testing will be required, particularly for the authentication system and data processing pipelines.

**Estimated Effort:** 3-4 weeks for complete migration and testing
**Risk Level:** Medium-High due to major version updates
**Success Criteria:** All tests pass, performance maintained or improved, new features functional