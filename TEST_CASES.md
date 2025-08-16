# 🧪 Dream Journal Analyzer - GUI Test Cases

## Test Environment Setup
- **Application**: Dream Journal Analyzer
- **Entry Point**: `python main_gui.py`
- **Database**: SQLite (dreams.db - created automatically)
- **Expected Result**: All tests should pass without errors

---

## 📝 Test Category 1: Dream Entry Form

### Test Case 1.1: Basic Dream Entry
**Objective**: Test basic dream recording functionality
**Steps**:
1. Launch the application
2. Verify "📝 New Dream" tab is active by default
3. Fill in the form:
   - Title: "Flying Over Mountains"
   - Date: Leave empty (should default to today)
   - Description: "I was flying over beautiful snow-capped mountains. The feeling was incredible and peaceful. I could control my flight direction by thinking about it."
   - Mood Before Sleep: Set to 7
   - Mood After Dream: Set to 9
   - Sleep Quality: Set to 8
   - Check "Lucid Dream" checkbox
   - Tags: "flying, mountains, peaceful, lucid"
4. Click "💾 Save Dream"

**Expected Results**:
- Success message appears
- Form clears after saving
- Sidebar statistics update
- Status bar shows "Dream saved successfully"

### Test Case 1.2: Dream Analysis
**Objective**: Test AI analysis functionality
**Steps**:
1. Fill in dream entry form with:
   - Title: "Nightmare Chase"
   - Description: "I was being chased by a dark figure through a scary forest. I felt terrified and couldn't run fast enough. My heart was pounding and I woke up sweating."
   - Check "Nightmare" checkbox
   - Tags: "chase, scary, forest, fear"
2. Click "🔍 Analyze Dream" (before saving)

**Expected Results**:
- Analysis window opens
- Shows sentiment analysis (should be negative)
- Displays emotions detected (fear, anxiety)
- Identifies themes (chase, forest)
- Shows complexity analysis
- Provides meaningful insights

### Test Case 1.3: Form Validation
**Objective**: Test input validation
**Steps**:
1. Try to save with empty title - should show error
2. Try to save with empty description - should show error
3. Enter invalid date format "2024/12/32" - should show error
4. Enter valid date "2024-01-15" - should accept

**Expected Results**:
- Appropriate error messages for invalid inputs
- Form accepts valid inputs
- Date validation works correctly

### Test Case 1.4: Form Controls
**Objective**: Test all form controls
**Steps**:
1. Test all sliders (mood before, mood after, sleep quality)
2. Test all checkboxes (lucid, nightmare, recurring)
3. Test "🗑️ Clear Form" button
4. Test tags with special characters and commas

**Expected Results**:
- Sliders update labels correctly (1-10)
- Checkboxes toggle properly
- Clear button resets all fields
- Tags parse correctly with commas

---

## 📚 Test Category 2: Dream List Management

### Test Case 2.1: View Dream List
**Objective**: Test dream list display
**Steps**:
1. Click "📚 Dream List" tab
2. Verify dreams are displayed chronologically
3. Check date and title formatting

**Expected Results**:
- Dreams listed with date and truncated title
- Most recent dreams at top
- Scrollbar appears if many dreams

### Test Case 2.2: Edit Dream
**Objective**: Test dream editing functionality
**Steps**:
1. In Dream List, double-click on a dream entry
2. Verify form populates with dream data
3. Modify the title and add new tags
4. Click "💾 Update Dream"

**Expected Results**:
- Form switches to edit mode
- All fields populate correctly
- Button changes to "Update Dream"
- Changes save successfully
- Returns to "Save Dream" after update

### Test Case 2.3: Delete Dream
**Objective**: Test dream deletion
**Steps**:
1. Select a dream in the list
2. Click "🗑️ Delete Selected"
3. Confirm deletion in dialog
4. Test canceling deletion

**Expected Results**:
- Confirmation dialog appears
- Dream deleted if confirmed
- Dream remains if canceled
- List refreshes after deletion
- Statistics update

### Test Case 2.4: List Navigation
**Objective**: Test list interaction
**Steps**:
1. Test scrolling through long lists
2. Test selecting different dreams
3. Test "🔄 Refresh List" button

**Expected Results**:
- Smooth scrolling
- Selection highlights correctly
- Refresh updates the list

---

## 🔍 Test Category 3: Search Functionality

### Test Case 3.1: Basic Search
**Objective**: Test search functionality
**Steps**:
1. Click "🔍 Search" tab
2. Enter search term "flying"
3. Click "🔍 Search"

**Expected Results**:
- Results show dreams containing "flying"
- Results display with date and title
- Status shows number of results found

### Test Case 3.2: Advanced Search
**Objective**: Test various search scenarios
**Steps**:
1. Search for partial words: "fly"
2. Search for multiple words: "flying mountains"
3. Search for tags: "lucid"
4. Search for emotions: "scared"
5. Search with no results: "xyz123"

**Expected Results**:
- Partial matches work
- Multiple word searches work
- Tag searches work
- Emotion searches work
- "No dreams found" message for no results

### Test Case 3.3: Search Edge Cases
**Objective**: Test search edge cases
**Steps**:
1. Search with empty field
2. Search with special characters
3. Search with very long terms

**Expected Results**:
- Appropriate handling of edge cases
- No crashes or errors
- Meaningful feedback to user

---

## 📊 Test Category 4: Analytics Dashboard

### Test Case 4.1: Statistics Display
**Objective**: Test analytics dashboard
**Steps**:
1. Click "📊 Analytics" tab
2. Verify statistics display correctly
3. Check all stat categories

**Expected Results**:
- Total dreams count matches actual
- Lucid dreams, nightmares counts correct
- Average mood and sleep quality calculated
- Statistics grid displays properly

### Test Case 4.2: Trends Analysis
**Objective**: Test trends functionality
**Steps**:
1. Add several dreams over different dates
2. View analytics dashboard
3. Check trends section

**Expected Results**:
- Recent trends show correctly
- Date ranges work properly
- Calculations are accurate

### Test Case 4.3: Statistics Updates
**Objective**: Test real-time statistics
**Steps**:
1. Note current statistics
2. Add a new dream
3. Return to analytics
4. Verify statistics updated

**Expected Results**:
- Statistics update automatically
- All counts increment correctly
- Averages recalculate properly

---

## ⚙️ Test Category 5: Settings & Data Management

### Test Case 5.1: Theme Switching
**Objective**: Test appearance modes
**Steps**:
1. Click "⚙️ Settings" tab
2. Change appearance mode to "Light"
3. Change to "Dark"
4. Change to "System"

**Expected Results**:
- Interface changes themes immediately
- All elements adapt to new theme
- Theme persists across sessions

### Test Case 5.2: Export Dreams
**Objective**: Test data export
**Steps**:
1. Click "📤 Export Dreams"
2. Choose save location
3. Save as JSON file
4. Open file to verify content

**Expected Results**:
- File dialog opens
- JSON file created successfully
- File contains all dream data
- Data is properly formatted

### Test Case 5.3: Import Dreams
**Objective**: Test data import
**Steps**:
1. Create backup of current dreams
2. Delete some dreams
3. Click "📥 Import Dreams"
4. Select previously exported file
5. Verify dreams restored

**Expected Results**:
- File dialog opens
- Dreams import successfully
- No duplicate entries created
- Statistics update correctly

---

## 🔄 Test Category 6: Integration & Workflow

### Test Case 6.1: Complete Workflow
**Objective**: Test end-to-end workflow
**Steps**:
1. Record 3 different dreams with various characteristics
2. Analyze each dream
3. Search for specific content
4. Edit one dream
5. Delete one dream
6. Export data
7. View analytics

**Expected Results**:
- All operations complete successfully
- Data consistency maintained
- No errors or crashes
- Statistics remain accurate

### Test Case 6.2: Data Persistence
**Objective**: Test data persistence
**Steps**:
1. Add several dreams
2. Close application
3. Reopen application
4. Verify all data present

**Expected Results**:
- All dreams persist after restart
- Statistics remain accurate
- Settings preserved
- No data loss

### Test Case 6.3: Error Handling
**Objective**: Test error scenarios
**Steps**:
1. Try operations with no dreams in database
2. Test with very long dream descriptions (1000+ words)
3. Test with special characters in all fields
4. Test rapid clicking of buttons

**Expected Results**:
- Graceful handling of edge cases
- No application crashes
- Appropriate error messages
- Application remains stable

---

## 🎯 Test Category 7: Performance & Usability

### Test Case 7.1: Performance with Large Dataset
**Objective**: Test with many dreams
**Steps**:
1. Import or create 50+ dreams
2. Test list loading speed
3. Test search performance
4. Test analytics calculation speed

**Expected Results**:
- Reasonable loading times
- Smooth scrolling
- Fast search results
- Quick analytics updates

### Test Case 7.2: UI Responsiveness
**Objective**: Test interface responsiveness
**Steps**:
1. Resize application window
2. Test with different screen resolutions
3. Test tab switching speed
4. Test form responsiveness

**Expected Results**:
- Interface adapts to window size
- Elements remain accessible
- Fast tab switching
- Responsive form controls

### Test Case 7.3: Memory Usage
**Objective**: Test resource usage
**Steps**:
1. Monitor memory usage during extended use
2. Test with large dream descriptions
3. Test analysis on multiple dreams

**Expected Results**:
- Reasonable memory consumption
- No memory leaks
- Stable performance over time

---

## 🚨 Critical Test Scenarios

### Critical Test 1: Database Corruption Recovery
**Steps**:
1. Backup dreams.db file
2. Corrupt the database file
3. Try to launch application
4. Restore from backup

### Critical Test 2: Missing Dependencies
**Steps**:
1. Temporarily rename a required module
2. Try to launch application
3. Verify error handling

### Critical Test 3: Concurrent Access
**Steps**:
1. Try running multiple instances
2. Test data consistency

---

## ✅ Test Completion Checklist

- [ ] All dream entry functions work
- [ ] Dream analysis provides meaningful results
- [ ] List management (view, edit, delete) works
- [ ] Search finds relevant dreams
- [ ] Analytics display correctly
- [ ] Export/import functions properly
- [ ] Theme switching works
- [ ] Application handles errors gracefully
- [ ] Data persists across sessions
- [ ] Performance is acceptable
- [ ] UI is responsive and user-friendly

---

## 📋 Bug Reporting Template

If you find any issues during testing:

**Bug Title**: [Brief description]
**Steps to Reproduce**: 
1. Step 1
2. Step 2
3. Step 3

**Expected Result**: [What should happen]
**Actual Result**: [What actually happened]
**Severity**: [Critical/High/Medium/Low]
**Screenshots**: [If applicable]

---

## 🎉 Testing Tips

1. **Test with realistic data**: Use actual dream descriptions
2. **Test edge cases**: Empty fields, very long text, special characters
3. **Test user workflows**: Complete realistic usage scenarios
4. **Test error conditions**: Invalid inputs, missing files
5. **Test performance**: Large datasets, rapid interactions
6. **Test persistence**: Close/reopen application frequently

Happy Testing! 🧪✨